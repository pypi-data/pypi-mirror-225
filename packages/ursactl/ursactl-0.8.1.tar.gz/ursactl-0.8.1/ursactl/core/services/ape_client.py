"""
APE Service client
"""

from json import dumps
import jsonschema

from ._base import Base

LIST_TRANSFORMS_QUERY = """\
query list_transforms($id: String!) {
    project(handleName: $id) {
        transforms {
            id
            name
            path
            type
            isSynced
            tags
        }
    }
}
"""

CREATE_TRANSFORM_MUTATION = """\
mutation create_transform($input: CreateTransformInput!) {
    createTransform(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
            path
        }
    }
}
"""

SYNC_TRANSFORM_MUTATION = """\
mutation sync_transform($input: SyncTransformInput!) {
    syncTransform(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
            path
        }
    }
}
"""

UPDATE_TRANSFORM_MUTATION = """\
mutation update_transform($id: ID!, $input: UpdateTransformInput!) {
    updateTransform(id: $id, input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
            path
        }
    }
}
"""

GET_TRANSFORM_BY_ID_QUERY = """\
query get_transform($id: ID!) {
    transform(id: $id) {
        path
        description
        configurationSchema
        type
        tags
        isSynced
    }
}
"""

GET_TRANSFORM_BY_PATH_QUERY = """\
query get_transform($path: String!, $project: String!) {
    project(handleName: $project) {
        transforms(limit: 1, filter: { path: { eq: $path } }) {
            id
            path
            description
            configurationSchema
            type
            tags
            isSynced
        }
    }
}
"""

DELETE_TRANSFORM_MUTATION = """\
mutation delete_transform($id: ID!) {
    deleteTransform(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

DELETE_SYNCED_TRANSFORM_MUTATION = """\
mutation delete_synced_transform($id: ID!) {
    deleteSyncedTransform(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

CREATE_GENERATOR_MUTATION = """\
mutation create_generator($input: CreateGeneratorInput!) {
    createGenerator(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

SYNC_GENERATOR_MUTATION = """\
mutation sync_generator($input: SyncGeneratorInput!) {
    syncGenerator(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

UPDATE_GENERATOR_MUTATION = """\
mutation update_generator($id: ID!, $input: UpdateGeneratorInput!) {
    updateGenerator(id: $id, input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

LIST_GENERATORS_FOR_PROJECT_QUERY = """\
query list_generators($id: String!) {
    project(handleName: $id) {
        generators {
            id
            path
            isSynced
            transform { type path project { name user { handle } } }
            tags
        }
    }
}
"""

GET_GENERATOR_BY_ID_QUERY = """\
query get_generator($id: ID!) {
    generator(id: $id) {
        path
        project { id }
    }
}
"""

GET_GENERATOR_BY_PATH_QUERY = """\
query get_generator($path: String!, $project_id: String!) {
    project(handleName: $project_id) {
        generators(limit: 1, filter: { path: { eq: $path } }) {
           id
        }
    }
}
"""

DELETE_GENERATOR_MUTATION = """\
mutation delete_generator($id: ID!) {
    deleteGenerator(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

DELETE_SYNCED_GENERATOR_MUTATION = """\
mutation delete_synced_generator($id: ID!) {
    deleteSyncedGenerator(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

CREATE_PIPELINE_MUTATION = """\
mutation create_pipeline($input: CreatePipelineInput!) {
    createPipeline(input: $input) {
        errors {
            code
            message
            fields
            vars
        }
        result {
            id
            path
        }
    }
}
"""

SYNC_PIPELINE_MUTATION = """\
mutation sync_pipeline($input: SyncPipelineInput!) {
    syncPipeline(input: $input) {
        errors {
            code
            message
            fields
            vars
        }
        result {
            id
            path
        }
    }
}
"""

DELETE_PIPELINE_MUTATION = """\
mutation delete_pipeline($id: ID!) {
    deletePipeline(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

DELETE_SYNCED_PIPELINE_MUTATION = """\
mutation delete_synced_pipeline($id: ID!) {
    deleteSyncedPipeline(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

UPDATE_PIPELINE_MUTATION = """\
mutation update_pipeline($id: ID!, $input: UpdatePipelineInput!) {
    updatePipeline(id: $id, input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

LIST_PIPELINES_FOR_PROJECT_QUERY = """\
query pipelines($id: String!) {
  project(handleName: $id) {
    pipelines {
      path
      id
      description
      isSynced
      tags
    }
  }
}
"""

LIST_PIPELINES_FOR_PROJECT_FULL_QUERY = """\
query pipelines($id: String!) {
  project(handleName: $id) {
    pipelines {
      path
      id
      isSynced
      description
      seeders
      generators
      tags
    }
  }
}
"""

RUN_PIPELINE_MUTATION = """\
mutation run_pipeline($input: RunPipelineInput!){
  runPipeline(input: $input) {
    errors {
        code
        message
        fields
    }
    result {
        id
        jobStatus
    }
  }
}
"""

SWEEP_PIPELINE_MUTATION = """\
mutation sweep_pipeline($input: SweepPipelineInput!){
  sweepPipeline(input: $input) {
    errors {
        code
        message
        fields
    }
    result {
        id
        jobStatus
    }
  }
}
"""

GET_PIPELINE_BY_ID_QUERY = """\
query get_pipeline($id: ID!) {
    pipeline(id: $id) {
        path
        project { id }
    }
}
"""

GET_PIPELINE_BY_PATH_QUERY = """\
query get_pipeline($path: String!, $project_id: String!) {
    project(handleName: $project_id) {
        pipelines(limit: 1, filter: { path: { eq: $path } }) {
           id
        }
    }
}
"""

LIST_PIPELINE_RUNS_BY_PROJECT = """\
query get_pipeline_runs($id: String!) {
    project(handleName: $id) {
        pipelines {
            path
            pipelineRuns {
                id
                jobStatus
                dataset { path }
            }
        }
    }
}
"""

LIST_PIPELINE_RUNS_BY_PIPELINE = """\
query get_pipeline_runs($id: ID!) {
    pipeline(id: $id) {
        path
        pipelineRuns {
            id
            jobStatus
            dataset { path }
        }
    }
}
"""

GET_PIPELINE_RUN = """\
query get_pipeline_run($id: ID!) {
    pipelineRun(id: $id) {
        dataset { id }
        jobStatus
        provenance
        parameters
    }
}
"""

GET_PIPELINE_SWEEP = """\
query get_pipeline_sweep($id: ID!) {
    pipelineSweep(id: $id) {
        jobStatus
        pipelineRuns {
            id
            dataset { id }
            jobStatus
            provenance
            parameters
        }
    }
}
"""


class ApeClient(Base):
    """
    Client providing access to the APE service.
    """
    def list_transforms(self, project_uuid=None):
        """
        Returns a list of available transforms.
        """

        query_response = self.raw_query(query=LIST_TRANSFORMS_QUERY, variables={
            'id': project_uuid
        })

        return query_response['data']['project']['transforms']

    def get_transform(self, uuid=None, path=None, project_uuid=None):
        """
        Returns more detail about the transform.
        """
        if uuid is not None:
            query_response = self.raw_query(query=GET_TRANSFORM_BY_ID_QUERY, variables={
                'id': uuid
            })

            return query_response['data']['transform']
        elif path is not None and path.find(':') == -1 and project_uuid is not None:
            query_response = self.raw_query(query=GET_TRANSFORM_BY_PATH_QUERY, variables={
                'path': path,
                'project': project_uuid
            })
            if query_response['data']['project']['transforms']:
                return query_response['data']['project']['transforms'][0]
        elif path is not None and path.find(':') != -1:
            bits = path.split(':', maxsplit=1)
            query_response = self.raw_query(query=GET_TRANSFORM_BY_PATH_QUERY, variables={
                'path': bits[1],
                'project': bits[0]
            })
            if query_response['data']['project']['transforms']:
                return query_response['data']['project']['transforms'][0]
        return None

    def create_transform(self,
                         project_uuid=None,
                         name=None,
                         path=None,
                         inputs=None,
                         outputs=None,
                         implementation=None,
                         description=None,
                         configuration_schema=None,
                         type=None,
                         tags=None):
        """
        Create a transform. This will do some light checking before sending the
        request. More extensive checking is done on the server.
        """
        if project_uuid is None:
            raise AttributeError("transforms must be assigned to a project.")
        if type not in ["seeder", "mapper", "reducer"]:
            raise AttributeError("transform type must be one of seeder, mapper, or reducer.")
        if implementation is None:
            raise AttributeError("transform implementation must be provided.")
        if path is None:
            raise AttributeError("transform path must be provided.")
        if configuration_schema is not None:
            jsonschema.Draft4Validator.check_schema(configuration_schema)
        variables = {
            'input': {
                'project': project_uuid,
                'type': type,
                'implementation': implementation,
                'path': path,
                'name': name,
                'configurationSchema': dumps(configuration_schema)
            }
        }
        if outputs is not None:
            variables['input']['outputs'] = dumps(outputs)
        if inputs is not None:
            variables['input']['inputs'] = dumps(inputs)
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=CREATE_TRANSFORM_MUTATION, variables=variables)

        return result['data']['createTransform']['result']

    def sync_transform(self,
                       project_uuid=None,
                       name=None,
                       path=None,
                       inputs=None,
                       outputs=None,
                       implementation=None,
                       description=None,
                       configuration_schema=None,
                       type=None,
                       tags=None):
        """
        Sync a transform. This will do some light checking before sending the
        request. More extensive checking is done on the server.
        """
        if project_uuid is None:
            raise AttributeError("transforms must be assigned to a project.")
        if type not in ["seeder", "mapper", "reducer"]:
            raise AttributeError("transform type must be one of seeder, mapper, or reducer.")
        if implementation is None:
            raise AttributeError("transform implementation must be provided.")
        if path is None:
            raise AttributeError("transform path must be provided.")
        if configuration_schema is not None:
            jsonschema.Draft4Validator.check_schema(configuration_schema)
        variables = {
            'input': {
                'project': project_uuid,
                'type': type,
                'implementation': implementation,
                'path': path,
                'name': name,
                'configurationSchema': dumps(configuration_schema)
            }
        }
        if outputs is not None:
            variables['input']['outputs'] = dumps(outputs)
        if inputs is not None:
            variables['input']['inputs'] = dumps(inputs)
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=SYNC_TRANSFORM_MUTATION, variables=variables)

        return result['data']['syncTransform']['result']

    def update_transform(self,  # noqa: C901
                         project_uuid=None,
                         name=None,
                         path=None,
                         inputs=None,
                         outputs=None,
                         implementation=None,
                         description=None,
                         configuration_schema=None,
                         type=None,
                         tags=None):
        """
        Update a transform. This will do some light checking before sending the
        request. More extensive checking is done on the server.
        """
        if project_uuid is None:
            raise AttributeError("transforms must be assigned to a project.")
        if type not in ["seeder", "mapper", "reducer"]:
            raise AttributeError("transform type must be one of seeder, mapper, or reducer.")
        if implementation is None:
            raise AttributeError("transform implementation must be provided.")
        if path is None:
            raise AttributeError("transform path must be provided.")
        if configuration_schema is not None:
            jsonschema.Draft4Validator.check_schema(configuration_schema)
        variables = {
            'input': {
                'type': type,
                'implementation': implementation,
                'path': path,
                'name': name,
                'configurationSchema': dumps(configuration_schema)
            }
        }
        if outputs is not None:
            variables['input']['outputs'] = dumps(outputs)
        if inputs is not None:
            variables['input']['inputs'] = dumps(inputs)
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        algo = self.get_transform(path=path, project_uuid=project_uuid)
        if algo is None:
            return {}
        variables['id'] = algo['id']
        result = self.raw_query(query=UPDATE_TRANSFORM_MUTATION, variables=variables)

        return result['data']['updateTransform']

    def delete_transform(self, id, project_uuid=None):
        """
        Deletes the transform.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            algo = self.get_transform(path=id, project_uuid=project_uuid)
            if algo is None:
                return {}
            variables = {'id': algo['id']}

        result = self.raw_query(query=DELETE_TRANSFORM_MUTATION, variables=variables)

        return result['data']['deleteTransform']

    def delete_synced_transform(self, id, project_uuid=None):
        """
        Deletes the transform.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            algo = self.get_transform(path=id, project_uuid=project_uuid)
            if algo is None:
                return {}
            variables = {'id': algo['id']}

        result = self.raw_query(query=DELETE_SYNCED_TRANSFORM_MUTATION, variables=variables)

        return result['data']['deleteSyncedTransform']

    def list_generators(self, project_uuid=None):
        """
        List generators given a transform or project scope. If no scope, then all
        generators for an account.
        """
        if project_uuid is None:
            raise AttributeError("Project id must be provided.")
        query = LIST_GENERATORS_FOR_PROJECT_QUERY
        variables = {'id': project_uuid}

        query_response = self.raw_query(query=query, variables=variables)

        if 'errors' in query_response:
            return []
        return query_response['data']['project']['generators']

    def create_generator(self,
                         project_uuid=None,
                         path=None,
                         description=None,
                         transform=None,
                         transform_configuration=None,
                         extract=None,
                         load=None,
                         tags=None):
        """
        Creates a generator. This will do some checking before sending the request to make sure
        the request is reasonable.
        """
        transform_rec = self.get_transform(project_uuid=project_uuid, path=transform)
        if transform_rec is None:
            raise ValueError(f"The transform ({transform}) is not defined.")
        if transform_rec['type'] != 'seeder' and extract is None:
            raise ValueError("Non-seeding generators require an 'extract' query.")
        jsonschema.validate(instance=transform_configuration, schema=transform_rec['configurationSchema'])

        variables = {
            'input': {
                'path': path,
                'project': project_uuid,
                'transform': transform,
                'configuration': dumps(transform_configuration),
                'extract': extract,
                'load': load
            }
        }
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=CREATE_GENERATOR_MUTATION, variables=variables)

        return result['data']['createGenerator']

    def sync_generator(self,
                       project_uuid=None,
                       path=None,
                       description=None,
                       transform=None,
                       transform_configuration=None,
                       extract=None,
                       load=None,
                       tags=None):
        """
        Syncs a generator. This will do some checking before sending the request to make sure
        the request is reasonable.
        """
        transform_rec = self.get_transform(project_uuid=project_uuid, path=transform)
        if transform_rec is None:
            raise ValueError(f"The transform ({transform}) is not defined.")
        if transform_rec['type'] != 'seeder' and extract is None:
            raise ValueError("Non-seeding generators require an 'extract' query.")
        jsonschema.validate(instance=transform_configuration, schema=transform_rec['configurationSchema'])

        variables = {
            'input': {
                'path': path,
                'project': project_uuid,
                'transform': transform,
                'configuration': dumps(transform_configuration),
                'extract': extract,
                'load': load
            }
        }
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=SYNC_GENERATOR_MUTATION, variables=variables)

        return result['data']['syncGenerator']

    def update_generator(self,
                         project_uuid=None,
                         path=None,
                         description=None,
                         transform=None,
                         transform_configuration=None,
                         extract=None,
                         load=None,
                         tags=None):
        """
        Creates a generator. This will do some checking before sending the request to make sure
        the request is reasonable.
        """
        transform_rec = self.get_transform(project_uuid=project_uuid, path=transform)
        if transform_rec is None:
            raise ValueError(f"The transform ({transform}) is not defined.")
        if transform_rec['type'] != 'seeder' and extract is None:
            raise ValueError("Non-seeding generators require an 'extract' query.")
        jsonschema.validate(instance=transform_configuration, schema=transform_rec['configurationSchema'])

        variables = {
            'input': {
                'path': path,
                'transform': transform,
                'configuration': dumps(transform_configuration),
                'extract': extract,
                'load': load
            }
        }
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags
        generator = self.get_generator(path=path, project_uuid=project_uuid)
        if generator is None:
            return {}
        variables['id'] = generator['id']
        result = self.raw_query(query=UPDATE_GENERATOR_MUTATION, variables=variables)

        return result['data']['updateGenerator']

    def get_generator(self, uuid=None, path=None, project_uuid=None):
        """
        Returns more detail about the generator.
        """
        if uuid is not None:
            query_response = self.raw_query(query=GET_GENERATOR_BY_ID_QUERY, variables={
                'id': uuid
            })

            return query_response['data']['generator']
        elif path is not None and project_uuid is not None:
            query_response = self.raw_query(query=GET_GENERATOR_BY_PATH_QUERY, variables={
                'path': path,
                'project_id': project_uuid
            })
            return query_response['data']['project']['generators'][0]
        return None

    def delete_generator(self, id, project_uuid=None):
        """
        Deletes the generator.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            generator = self.get_generator(path=id, project_uuid=project_uuid)
            if generator is None:
                return {}
            variables = {'id': generator['id']}

        result = self.raw_query(query=DELETE_GENERATOR_MUTATION, variables=variables)

        return result['data']['deleteGenerator']

    def delete_synced_generator(self, id, project_uuid=None):
        """
        Deletes a synced generator.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            generator = self.get_generator(path=id, project_uuid=project_uuid)
            if generator is None:
                return {}
            variables = {'id': generator['id']}

        result = self.raw_query(query=DELETE_SYNCED_GENERATOR_MUTATION, variables=variables)

        return result['data']['deleteSyncedGenerator']

    def list_pipelines(self, project_uuid=None, all=False):
        """
        List pipelines given a project scope. If no scope, then all
        pipelines for an account.
        """

        variables = {}
        query = LIST_PIPELINES_FOR_PROJECT_QUERY
        if all:
            query = LIST_PIPELINES_FOR_PROJECT_FULL_QUERY
        variables['id'] = project_uuid

        query_response = self.raw_query(query=query, variables=variables)

        if 'errors' in query_response:
            return []

        return query_response['data']['project']['pipelines']

    def create_pipeline(self, project_uuid=None, description=None, path=None, seeders=None, generators=None, tags=None):
        """
        Creates a pipeline.
        """
        variables = {
            'input': {
                'path': path,
                'project': project_uuid,
                'seeders': [],
                'generators': []
            }
        }

        if generators is not None:
            variables['input']['generators'] = [
                self._marshal_generator(label, generator) for label, generator in generators.items()]
        if seeders is not None:
            variables['input']['seeders'] = [self._marshal_seeder(seeder) for seeder in seeders]
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags

        result = self.raw_query(query=CREATE_PIPELINE_MUTATION, variables=variables)
        if 'errors' in result:
            return {"accepted": False}

        return result['data']['createPipeline']

    def sync_pipeline(self, project_uuid=None, description=None, path=None, seeders=None, generators=None, tags=None):
        """
        Syncs a pipeline.
        """
        variables = {
            'input': {
                'path': path,
                'project': project_uuid,
                'seeders': [],
                'generators': []
            }
        }

        if generators is not None:
            variables['input']['generators'] = [
                self._marshal_generator(label, generator) for label, generator in generators.items()]
        if seeders is not None:
            variables['input']['seeders'] = [self._marshal_seeder(seeder) for seeder in seeders]
        if description is not None:
            variables['input']['description'] = description
        if tags is not None:
            variables['input']['tags'] = tags

        result = self.raw_query(query=SYNC_PIPELINE_MUTATION, variables=variables)
        if 'errors' in result:
            return {"accepted": False}

        return result['data']['syncPipeline']

    def update_pipeline(self, project_uuid=None, description=None, path=None, seeders=None, generators=None):
        """
        Updates a pipeline.
        """
        variables = {
            'input': {
                'path': path,
                'seeders': [],
                'generators': []
            }
        }

        if generators is not None:
            variables['input']['generators'] = [
                self._marshal_generator(label, generator) for label, generator in generators.items()]
        if seeders is not None:
            variables['input']['seeders'] = [self._marshal_seeder(seeder) for seeder in seeders]
        if description is not None:
            variables['input']['description'] = description
        pipeline = self.get_pipeline(path=path, project_uuid=project_uuid)
        if pipeline is None:
            return {}
        variables['id'] = pipeline['id']
        result = self.raw_query(query=UPDATE_PIPELINE_MUTATION, variables=variables)
        if 'errors' in result:
            return {"accepted": False}

        return result['data']['updatePipeline']

    def get_pipeline(self, uuid=None, path=None, project_uuid=None):
        """
        Returns more detail about the pipeline.
        """
        if uuid is not None:
            query_response = self.raw_query(query=GET_PIPELINE_BY_ID_QUERY, variables={
                'id': uuid
            })

            return query_response['data']['pipeline']
        elif path is not None and project_uuid is not None:
            query_response = self.raw_query(query=GET_PIPELINE_BY_PATH_QUERY, variables={
                'path': path,
                'project_id': project_uuid
            })
            return query_response['data']['project']['pipelines'][0]
        return None

    def get_pipeline_run(self, uuid):
        """
        Returns more detail about the pipeline run.
        """
        query_response = self.raw_query(query=GET_PIPELINE_RUN, variables={
            'id': uuid
        })
        return query_response['data']['pipelineRun']

    def get_pipeline_sweep(self, uuid):
        """
        Returns more detail about the pipeline sweep.
        """
        query_response = self.raw_query(query=GET_PIPELINE_SWEEP, variables={
            'id': uuid
        })
        return query_response['data']['pipelineSweep']

    def list_pipeline_runs(self, pipeline_id=None, project_uuid=None):
        """
        List pipeline runs for a pipeline.
        """
        if pipeline_id is not None:
            if self.is_uuid(pipeline_id):
                variables = {'id': pipeline_id}
            else:
                pipeline = self.get_pipeline(path=pipeline_id, project_uuid=project_uuid)
                if pipeline is None:
                    return []
                variables = {'id': pipeline['id']}
            query_response = self.raw_query(query=LIST_PIPELINE_RUNS_BY_PIPELINE, variables=variables)
            pipeline_path = query_response['data']['pipeline']['path']
            return [{'pipeline': pipeline_path, **run} for run in query_response['data']['pipeline']['pipelineRuns']]
        else:
            variables = {'id': project_uuid}
            query_response = self.raw_query(query=LIST_PIPELINE_RUNS_BY_PROJECT, variables=variables)
            return [
                {
                    'pipeline': pipeline['path'],
                    'dataset': self._get_dataset_path(run['dataset']),
                    'jobStatus': run['jobStatus']
                }
                for pipeline in query_response['data']['project']['pipelines']
                for run in pipeline['pipelineRuns']
            ]

    @staticmethod
    def _get_dataset_path(dataset):
        try:
            path = dataset['path']
        except (KeyError, TypeError):
            path = ''
        return path

    def _marshal_generator(self, label, values):
        new_values = self._marshal_seeder(values)
        new_values['label'] = label
        if 'dependsOn' not in new_values:
            new_values['dependsOn'] = []
        return new_values

    def _marshal_seeder(self, values):
        new_values = values.copy()
        if 'generator' in values and 'configuration' in values['generator']:
            new_values['generator'] = values['generator'].copy()
            new_values['generator']['configuration'] = dumps(values['generator']['configuration'])
        elif 'dataset' in values and 'configuration' in values['dataset']:
            new_values['dataset'] = values['dataset']['configuration'].copy()
            new_values['dataset']['path'] = values['dataset']['path']
        return new_values

    def delete_pipeline(self, id, project_uuid=None):
        """
        Deletes the pipeline.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            pipeline = self.get_pipeline(path=id, project_uuid=project_uuid)
            if pipeline is None:
                return {}
            variables = {'id': pipeline['id']}

        result = self.raw_query(query=DELETE_PIPELINE_MUTATION, variables=variables)

        return result['data']['deletePipeline']

    def delete_synced_pipeline(self, id, project_uuid=None):
        """
        Deletes the synced pipeline.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            pipeline = self.get_pipeline(path=id, project_uuid=project_uuid)
            if pipeline is None:
                return {}
            variables = {'id': pipeline['id']}

        result = self.raw_query(query=DELETE_SYNCED_PIPELINE_MUTATION, variables=variables)

        return result['data']['deleteSyncedPipeline']

    def run_pipeline(self, pipeline, parameters=None, sweep_parameters=None, project=None):
        """
        Runs the pipeline.
        """

        variables = {
            'input': {
                'pipeline': pipeline,
                'project': project
            }
        }
        query = RUN_PIPELINE_MUTATION
        result_key = 'runPipeline'
        if parameters is not None:
            variables['input']['parameters'] = dumps(parameters)
        if sweep_parameters is not None and any(sweep_parameters):
            variables['input']['sweptParameters'] = dumps(sweep_parameters)
            query = SWEEP_PIPELINE_MUTATION
            result_key = 'sweepPipeline'
        result = self.raw_query(query=query, variables=variables)
        return result['data'][result_key]
