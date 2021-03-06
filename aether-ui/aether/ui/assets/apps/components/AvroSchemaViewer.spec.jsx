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

/* global describe, it, expect */

import React from 'react'
import { mountWithIntl } from 'enzyme-react-intl'

import mockAvroSchema from '../../tests/mock/schema_input.mock.json'
import { AvroSchemaViewer } from '../components'

describe('AvroSchemaViewer', () => {
  it('should take a valid avro schema and render an avro visualizer', () => {
    const component = mountWithIntl(
      <AvroSchemaViewer schema={mockAvroSchema} highlight={{ 'person.forename': 1 }} />
    )
    expect(component.find('[data-qa^="group-title-"]').length).toEqual(9)
    expect(component.find('[data-qa="no-children-surname"]').html())
      .toContain('<span class="name">surname</span>')
    expect(component.find('[data-qa="no-children-forename"]').html())
      .toContain('<span class="name">forename</span><span class="type"> string,int</span>')
    expect(component.find('[data-qa="no-children-gender"]').html())
      .toContain('<span class="type"> (nullable)</span>')
    expect(component.find('[id="input_person.iterate_one.item"]').html())
      .toContain('<span class="name item">item</span>')
  })

  it('should take a invalid avro schema and render an invalid error message', () => {
    delete mockAvroSchema['name']
    const component = mountWithIntl(<AvroSchemaViewer schema={mockAvroSchema} />)
    expect(component.html()).toContain('You have provided an invalid AVRO schema.')
  })

  it('should render an empty avro schema viewer', () => {
    const component = mountWithIntl(<AvroSchemaViewer />)
    expect(component.html())
      .toContain('Your schema for this pipeline will be displayed here once you have added a valid source')
  })
})
