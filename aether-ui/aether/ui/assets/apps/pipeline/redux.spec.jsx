/*
 * Copyright (C) 2018 by eHealth Africa : http://www.eHealthAfrica.org
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/* global describe, it, expect, beforeEach */
import reducer, { types, selectedPipelineChanged,
  addPipeline, getPipelines, updatePipeline,
  INITIAL_PIPELINE, getPipelineById, publishPipeline } from './redux'
import { createStore, applyMiddleware } from 'redux'
import nock from 'nock'
import middleware from '../redux/middleware'
import mockPipelines from '../../tests/mock/pipelines.mock'
import { MAX_PAGE_SIZE } from '../utils/constants'

describe('Pipeline actions', () => {
  let store
  beforeEach(() => {
    // create a new store instance for each test
    store = createStore(
      reducer,
      applyMiddleware(...middleware)
    )
  })

  it('should return the initial redux store state', () => {
    expect(store.getState()).toEqual(
      INITIAL_PIPELINE
    )
  })

  it('should dispatch a selected pipeline changed action and update the redux store', () => {
    const selectedPipeline = {
      name: 'mock name',
      id: 1,
      errors: 0,
      entityTypes: 3,
      highlightDestination: [],
      highlightSource: {}
    }
    const expectedAction = {
      type: types.SELECTED_PIPELINE_CHANGED,
      payload: selectedPipeline
    }
    expect(selectedPipelineChanged(selectedPipeline)).toEqual(expectedAction)
    store.dispatch(selectedPipelineChanged(selectedPipeline))
    expect(store.getState().selectedPipeline).toEqual(
      selectedPipeline
    )
  })

  it('should create an action when adding a new pipeline and store in redux', () => {
    const newPipeline = { name: 'mock new name' }
    nock('http://localhost')
      .post('/api/pipelines/')
      .reply(200, Object.assign(newPipeline, { id: 'mockid', 'contracts': [] }))
    expect(typeof addPipeline(newPipeline)).toEqual('object')
    return store.dispatch(addPipeline(newPipeline))
      .then(res => {
        expect(store.getState().pipelineList[0].id).toEqual(
          'mockid'
        )
      })
  })

  it('should dispatch an update action and update redux store', () => {
    const pipeline = {
      'id': '1243563231',
      'pipeline': 2,
      'name': 'contract 2',
      'isInputReadOnly': false,
      'mapping_errors': null,
      'mapping': [],
      'output': null,
      'entity_types': [],
      'schema': null,
      'input': null,
      'highlightDestination': [],
      'highlightSource': {}
    }
    nock('http://localhost')
      .get(`/api/pipelines/?limit=${MAX_PAGE_SIZE}`)
      .reply(200, mockPipelines)

    nock('http://localhost')
      .put(`/api/pipelines/${pipeline.id}/`)
      .reply(200, pipeline)
    expect(typeof updatePipeline(pipeline)).toEqual('object')
    return store.dispatch(getPipelines())
      .then(() => {
        return store.dispatch(updatePipeline(pipeline))
          .then(() => {
            expect(store.getState().pipelineList[1]).toEqual(
              pipeline
            )
          })
      })
  })

  it('should try updating pipeline with wrong id and fail', () => {
    const wrongPipeline = {
      'id': 1001,
      'name': 'None existant pipeline ',
      'mapping_errors': null,
      'mapping': [],
      'output': null,
      'entity_types': [],
      'schema': null,
      'input': null,
      'pipeline': 100
    }
    nock('http://localhost')
      .get(`/api/pipelines/?limit=${MAX_PAGE_SIZE}`)
      .reply(200, mockPipelines)

    nock('http://localhost')
      .put(`/api/pipelines/${wrongPipeline.pipeline}/`)
      .reply(404)
    expect(typeof updatePipeline(wrongPipeline)).toEqual('object')
    return store.dispatch(getPipelines())
      .then(() => {
        return store.dispatch(updatePipeline(wrongPipeline))
          .then(res => {
            expect(store.getState().error).toEqual(
              { error: 'Not Found', message: 'Resource Not Found', status: 404 }
            )
          })
      })
  })

  it('should successfully get all pipelines and add to store', () => {
    nock('http://localhost')
      .get(`/api/pipelines/?limit=${MAX_PAGE_SIZE}`)
      .reply(200, mockPipelines)
    store.dispatch({ type: types.GET_ALL, payload: { results: [] } })
    expect(store.getState().pipelineList).toEqual([])
    return store.dispatch(getPipelines())
      .then(() => {
        expect(store.getState().pipelineList).toEqual(
          mockPipelines.transformed
        )
      })
  })

  it('should fail on getting all pipelines and store error', () => {
    nock('http://localhost')
      .get('/api/nojson.json')
      .reply(404)
    const NotFoundUrl = 'http://localhost/api/nojson.json'
    const action = () => ({
      types: ['', types.GET_ALL, types.PIPELINE_ERROR],
      promise: client => client.get(NotFoundUrl)
    }) // Sample usage of request middleware (client) plugged into redux
    const expectedStoreData = {
      pipelineList: [],
      selectedPipeline: null,
      error: { error: 'Not Found', message: 'Resource Not Found', status: 404 },
      notFound: null,
      publishSuccess: null,
      publishError: null,
      isNewPipeline: false
    }
    return store.dispatch(action())
      .then(() => {
        expect(store.getState()).toEqual(expectedStoreData)
      })
  })

  it('should dispatch an action to get pipeline and contract by id and set it as selected pipeline in the redux store', () => {
    const pipeline = {
      'id': 3,
      'name': 'Pipeline Mock 3',
      'contracts': [{
        'mapping_errors': null,
        'mapping': [],
        'output': null,
        'entity_types': [],
        'id': '124356323',
        'name': 'contract 3'
      }],
      'schema': null,
      'input': null
    }
    nock('http://localhost')
      .get(`/api/pipelines/${pipeline.id}/`)
      .reply(200, pipeline)
    expect(typeof getPipelineById(pipeline.id, pipeline.contracts[0].id)).toEqual('object')
    return store.dispatch(getPipelineById(pipeline.id, pipeline.contracts[0].id))
      .then(() => {
        expect(store.getState().selectedPipeline).toEqual(
          mockPipelines.transformed[2]
        )
      })
  })

  it('should dispatch a publish pipeline action and save response in the redux store', () => {
    const pipeline = mockPipelines.results[0]
    const selectedPipe = mockPipelines.transformed[0]
    nock('http://localhost')
      .post('/api/pipelines/1/publish/')
      .reply(200, pipeline)
    expect(typeof publishPipeline(pipeline.id, pipeline.contracts[0].id)).toEqual('object')
    store.dispatch(selectedPipelineChanged(selectedPipe))
    return store.dispatch(publishPipeline(pipeline.id, pipeline.contracts[0].id))
      .then(() => {
        expect(store.getState().publishSuccess).toEqual(
          true
        )
        expect(store.getState().publishError).toEqual(
          null
        )
      })
  })

  it('should dispatch a wrong publish pipeline action and save response in the redux store', () => {
    const returnedData = {
      error: ['error 1'],
      exists: ['exist 1']
    }
    nock('http://localhost')
      .post('/api/pipelines/100/publish/')
      .reply(400, returnedData)
    return store.dispatch(publishPipeline(100))
      .then(() => {
        expect(store.getState().publishError).toEqual(
          returnedData
        )
        expect(store.getState().publishSuccess).toEqual(
          null
        )
      })
  })
})
