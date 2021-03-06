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

import React, { Component } from 'react'
import { FormattedMessage, defineMessages, injectIntl } from 'react-intl'
import { connect } from 'react-redux'
import avro from 'avsc'

import { EntityTypeViewer } from '../../components'
import { deepEqual } from '../../utils'
import { updateContract } from '../redux'

const MESSAGES = defineMessages({
  missingIdError: {
    defaultMessage: 'The AVRO schemas MUST have an "id" field with type "string".',
    id: 'entitytype.missing.id.message'
  }
})

class EntityTypes extends Component {
  constructor (props) {
    super(props)

    this.state = {
      entityTypesSchema: this.parseProps(props),
      error: null
    }
  }

  componentWillReceiveProps (nextProps) {
    this.setState({
      entityTypesSchema: this.parseProps(nextProps),
      error: null
    })
  }

  parseProps (props) {
    const { entity_types: entityTypes } = props.selectedPipeline
    return entityTypes.length ? JSON.stringify(entityTypes, 0, 2) : ''
  }

  onSchemaTextChanged (event) {
    this.setState({
      entityTypesSchema: event.target.value
    })
  }

  notifyChange (event) {
    event.preventDefault()
    const { formatMessage } = this.props.intl

    try {
      // validate schemas
      const schemas = JSON.parse(this.state.entityTypesSchema)
      schemas.forEach(schema => {
        avro.parse(schema, { noAnonymousTypes: true, wrapUnions: false })
        // all entity types must have an "id" field with type "string"
        if (!schema.fields.find(field => field.name === 'id' && field.type === 'string')) {
          throw new Error(formatMessage(MESSAGES.missingIdError))
        }
      })
      this.props.updateContract({ ...this.props.selectedPipeline, entity_types: schemas })
    } catch (error) {
      this.setState({ error: error.message })
    }
  }

  hasChanged () {
    try {
      const schemas = JSON.parse(this.state.entityTypesSchema)
      return !deepEqual(schemas, this.props.selectedPipeline.entity_types)
    } catch (e) {
      return true
    }
  }

  render () {
    return (
      <div className='section-body'>
        <div className='section-left'>
          <EntityTypeViewer
            schema={this.props.selectedPipeline.entity_types}
            highlight={this.props.selectedPipeline.highlightDestination}
          />
        </div>

        <div className='section-right'>
          <form onSubmit={this.notifyChange.bind(this)}>
            <label className='form-label'>
              <FormattedMessage
                id='entitytype.empty.message'
                defaultMessage='Paste Entity Type definitions'
              />
            </label>

            <div className='textarea-header'>
              { this.state.error &&
                <div className='hint error-message'>
                  <h4 className='hint-title'>
                    <FormattedMessage
                      id='entitytype.invalid.message'
                      defaultMessage='You have provided invalid AVRO schemas.'
                    />
                  </h4>
                  { this.state.error }
                </div>
              }
            </div>

            <FormattedMessage id='entityTypeSchema.placeholder' defaultMessage='Enter your schemas'>
              {message => (
                <textarea
                  className={`input-d monospace ${this.state.error ? 'error' : ''}`}
                  value={this.state.entityTypesSchema}
                  onChange={this.onSchemaTextChanged.bind(this)}
                  placeholder={message}
                  rows='10'
                  disabled={this.props.selectedPipeline.is_read_only}
                />
              )}
            </FormattedMessage>

            <button type='submit' className='btn btn-d btn-primary mt-3' disabled={!this.hasChanged()}>
              <span className='details-title'>
                <FormattedMessage
                  id='entitytype.button.ok'
                  defaultMessage='Add to pipeline'
                />
              </span>
            </button>
          </form>
        </div>
      </div>
    )
  }
}

const mapStateToProps = ({ pipelines }) => ({
  selectedPipeline: pipelines.selectedPipeline
})

export default connect(mapStateToProps, { updateContract })(injectIntl(EntityTypes))
