import logging
import pandas as pd
import time
import urllib.parse
from typing import Union, List, Optional
from datahub.configuration.kafka import KafkaProducerConnectionConfig
from datahub.specific.dataset import DatasetPatchBuilder
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from datahub.ingestion.run.pipeline import Pipeline
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.emitter.kafka_emitter import DatahubKafkaEmitter, KafkaEmitterConfig
from datahub.cli import delete_cli
from datahub.emitter.mce_builder import (
    make_data_platform_urn, 
    make_dataset_urn, 
    make_domain_urn,
    make_user_urn,
    make_tag_urn,
    make_lineage_mce
)
from datahub.metadata.schema_classes import (
    AuditStampClass,
    ChangeTypeClass,
    DateTypeClass,
    DatasetPropertiesClass,
    DomainPropertiesClass,
    GlobalTagsClass, 
    OtherSchemaClass,
    SchemaFieldClass,
    SchemaFieldDataTypeClass,
    SchemaMetadataClass,
    StringTypeClass,
    OwnerClass,
    OwnershipClass,
    OwnershipTypeClass,
    TagAssociationClass,
    EditableDatasetPropertiesClass,
    InstitutionalMemoryClass,
    InstitutionalMemoryMetadataClass
)

# Configure logger
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

'''

General Helpers  

'''
def get_client(endpoint: str) -> DataHubGraph:
    config = DatahubClientConfig(
        server=endpoint,
        disable_ssl_verification=True
    )
    return DataHubGraph(config)

def get_dataset_source_url(endpoint: str, dataset_name: str) -> str:
    dataset_urn = make_dataset_urn(platform="s3", name=dataset_name, env="PROD")
    with get_client(endpoint=endpoint) as client:
        return client.get_aspect(
            entity_urn=dataset_urn,
            aspect_type=DatasetPropertiesClass,
            version=0
        ).customProperties['table_path']
    
def get_dataset_properties(endpoint: str, dataset_urn: str) -> str:
    with get_client(endpoint=endpoint) as client:
        return client.get_dataset_properties(
            entity_urn=dataset_urn
        )

def load_csv_dataset_as_pandas_dataframe(
    dataset:str, 
    minio_endpoint="http://minio-service.kubeflow.svc.cluster.local:9000", 
    datahub_endpoint="http://datahub-datahub-gms.datahub.svc.cluster.local:8080") -> pd.DataFrame:
    dataset_source_url = get_dataset_source_url(
        endpoint=datahub_endpoint,
        dataset_name=dataset
    )
    dataset_source_url = "s3://%s" % dataset_source_url
    #dataset_source_url = "s3://sources/get-sources-example/new%20zealand%20business%20demography%20statistics"    
    logger.info("Dataset source url -> %s" % dataset_source_url)
    return pd.read_csv(
        dataset_source_url,
        storage_options={
            "client_kwargs": {
                "endpoint_url": minio_endpoint,
                "aws_access_key_id": "minio",
                "aws_secret_access_key": "minio123"
            }
        }
    )



'''

Dataset Helpers  

'''
def upsert_datasets(dataset_urns: List[str],
                   platform_urn: str,
                   datahub_endpoint: str,
                   dataset_schema: List[SchemaFieldClass],
                   dataset_ver: int=0) -> None: 
    
    for dataset_urn in dataset_urns:
        event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=SchemaMetadataClass(
                schemaName="", 
                platform=platform_urn,
                version=dataset_ver, 
                hash="", 
                platformSchema=OtherSchemaClass(rawSchema="__insert raw schema here__"),
                lastModified=AuditStampClass(
                    time=1640692800000, actor="urn:li:corpuser:ingestion"
                ),
                fields=dataset_schema
            )
        )
        DatahubRestEmitter(gms_server=datahub_endpoint).emit(event)
        logger.info("Dataset %s should be upserted" % dataset_urn)


def upsert_dataset_custom_props(dataset_urn: str,
                   custom_props: List[tuple],
                   datahub_endpoint: str) -> None: 

    #dataset_urn = entityUrn
    for custom_prop in custom_props:
        with DatahubRestEmitter(gms_server=datahub_endpoint) as emitter:
            for patch_mcp in (
                DatasetPatchBuilder(dataset_urn)
                .add_custom_property(custom_prop[0], custom_prop[1])
                .build()
            ):
                emitter.emit(patch_mcp)
                log.info(f"Updated custom props on {dataset_urn} with {custom_prop[0]}={custom_prop[1]}")


def upsert_dataset_tags(dataset_urn: str,
                   tags_to_add: List[str],
                   datahub_endpoint: str) -> None: 
    
    graph = DataHubGraph(DatahubClientConfig(server=datahub_endpoint))
    current_tags: Optional[GlobalTagsClass] = graph.get_aspect(
        entity_urn=dataset_urn,
        aspect_type=GlobalTagsClass,
    )
    for tag_to_add in tags_to_add:
        tag_to_add=make_tag_urn(tag_to_add)
        tag_association_to_add = TagAssociationClass(tag=tag_to_add)
        need_write = False
        if current_tags:
            if tag_to_add not in [x.tag for x in current_tags.tags]:
                # tags exist, but this tag is not present in the current tags
                current_tags.tags.append(TagAssociationClass(tag_to_add))
                need_write = True
        else:
            current_tags = GlobalTagsClass(tags=[tag_association_to_add])
            need_write = True

        if need_write:
            event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
                entityUrn=dataset_urn,
                aspect=current_tags,
            )
            graph.emit(event)
            log.info(f"Tag {tag_to_add} added to dataset {dataset_urn}")
        else:
            log.info(f"Tag {tag_to_add} already exists, omitting write")


def upsert_dataset_description(dataset_urn: str,
                   documentation_to_add: str,
                   link_to_add: str,
                   link_description: str,
                   datahub_endpoint: str) -> None: 

    print(link_to_add)
    now = int(time.time() * 1000)
    current_timestamp = AuditStampClass(time=now, actor="urn:li:corpuser:ingestion")
    institutional_memory_element = InstitutionalMemoryMetadataClass(
        url=link_to_add,
        description=link_description,
        createStamp=current_timestamp,
    )
    graph = DataHubGraph(config=DatahubClientConfig(server=datahub_endpoint))
    current_editable_properties = graph.get_aspect(
        entity_urn=dataset_urn, aspect_type=EditableDatasetPropertiesClass
    )
    need_write = False
    if current_editable_properties:
        if documentation_to_add != current_editable_properties.description:
            current_editable_properties.description = documentation_to_add
            need_write = True
    else:
        # create a brand new editable dataset properties aspect
        current_editable_properties = EditableDatasetPropertiesClass(
            created=current_timestamp, description=documentation_to_add
        )
        need_write = True
    if need_write:
        event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=current_editable_properties,
        )
        graph.emit(event)
        log.info(f"Documentation added to dataset {dataset_urn}")
    else:
        log.info("Documentation already exists and is identical, omitting write")
    current_institutional_memory = graph.get_aspect(
        entity_urn=dataset_urn, aspect_type=InstitutionalMemoryClass
    )
    need_write = False
    if current_institutional_memory:
        if link_to_add not in [x.url for x in current_institutional_memory.elements]:
            current_institutional_memory.elements.append(institutional_memory_element)
            need_write = True
    else:
        # create a brand new institutional memory aspect
        current_institutional_memory = InstitutionalMemoryClass(
            elements=[institutional_memory_element]
        )
        need_write = True
    if need_write:
        event = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=current_institutional_memory,
        )
        graph.emit(event)
        log.info(f"Link {link_to_add} added to dataset {dataset_urn}")
    else:
        log.info(f"Link {link_to_add} already exists and is identical, omitting write")


def upsert_dataset_lineage(upstream_dataset_urn: str,
                           downstream_dataset_urn: str,
                           datahub_endpoint: str) -> None: 
 
    # Map pipeline to usecase
    lineage_mce = make_lineage_mce(
        [upstream_dataset_urn],
        downstream_dataset_urn
    )
    DatahubRestEmitter(gms_server=datahub_endpoint).emit_mce(lineage_mce)
    log.info(f"Lineage {lineage_mce} created")


def upsert_dataset_gitflow_lineage(dataset_urn: str,
                                   pipeline_name: str,  
                                   usecase_name: str,
                                   datahub_endpoint: str) -> None: 
 
    # Create / update datasets for pipeline and usecase
    pipeline_urn = make_dataset_urn(platform="github", name=pipeline_name)
    usecase_urn = make_dataset_urn(platform="github", name=usecase_name)
    upsert_datasets(dataset_urns=[pipeline_urn, usecase_urn],
                    platform_urn=make_data_platform_urn("github"),
                    datahub_endpoint=datahub_endpoint,
                    dataset_schema=[])
    # Connect usecase <> pipeline
    upsert_dataset_lineage(upstream_dataset_urn=usecase_urn,
                           downstream_dataset_urn=pipeline_urn,
                           datahub_endpoint=datahub_endpoint)
    # Connect pipeline <> dataset
    upsert_dataset_lineage(upstream_dataset_urn=pipeline_urn,
                           downstream_dataset_urn=dataset_urn,
                           datahub_endpoint=datahub_endpoint)
    
def upsert_dataset_ownership(dataset_urn: str,
                             owner_urn: str,
                             ownership_type: OwnershipTypeClass,
                             datahub_endpoint: str) -> None: 

    owner_class_to_add = OwnerClass(owner=owner_urn, type=ownership_type)
    ownership_to_add = OwnershipClass(owners=[owner_class_to_add])
    graph = DataHubGraph(DatahubClientConfig(server=datahub_endpoint))
    current_owners: Optional[OwnershipClass] = graph.get_aspect(
        entity_urn=dataset_urn, aspect_type=OwnershipClass
    )
    need_write = False
    if current_owners:
        if (owner_urn, ownership_type) not in [
            (x.owner, x.type) for x in current_owners.owners
        ]:
            # owners exist, but this owner is not present in the current owners
            current_owners.owners.append(owner_class_to_add)
            need_write = True
    else:
        # create a brand new ownership aspect
        current_owners = ownership_to_add
        need_write = True
    if need_write:
        event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=current_owners,
        )
        graph.emit(event)
        log.info(
            f"Owner {owner_urn}, type {ownership_type} added to dataset {dataset_urn}"
        )
    else:
        log.info(f"Owner {owner_urn} already exists, omitting write")


def delete_dataset_by_urn(dataset_urn: str,
                          datahub_endpoint: str) -> None: 

    rest_emitter = DatahubRestEmitter(gms_server=datahub_endpoint)
    delete_cli._delete_one_urn(urn=dataset_urn, soft=False, cached_emitter=rest_emitter)
    log.info(f"Deleted dataset {dataset_urn}")