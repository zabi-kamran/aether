import React, { Component } from 'react'
import {
  FormattedDate,
  FormattedMessage,
  FormattedRelative,
  FormattedTime
} from 'react-intl'

import { flatten, inflate } from '../utils/types'
import { JSONViewer } from '../components'

const SEPARATOR = '¬¬¬'  // very uncommon string

export default class ResponsesList extends Component {
  render () {
    const {list} = this.props

    if (list.length === 0) {
      return <div data-qa='responses-list-empty' />
    }

    // the first entry will decide the table columns
    const columns = Object.keys(flatten(list[0].data, SEPARATOR))

    return (
      <div data-qa='responses-list' className='x-0'>
        <div className='survey-content'>
          <table className='table table-sm'>
            { this.renderHeader(columns) }
            <tbody>
              { list.map((response, index) => this.renderResponse(response, index, columns)) }
            </tbody>
          </table>
        </div>
      </div>
    )
  }

  renderHeader (columns) {
    /****************************************************************
        Data
        ====
        {
          a: {
            b: {
              c: 1,
              d: 2
            },
            e: {
              f: true
            },
            g: []
          },
          h: 0
        }

        Table header
        ============
        +---+------------+------+----------------+---+
        | # | Submitted  | Data | A              | H |
        |   |            |      +-------+---+----+   |
        |   |            |      | B     | E | G  |   |
        |   |            |      +---+---+---+    |   |
        |   |            |      | C | D | F |    |   |
        +---+------------+------+---+---+---+----+---+
        | 1 | 1999-01-01 | #### | 1 | 2 | T | [] | 0 |
        +---+------------+------+---+---+---+----+---+

    ****************************************************************/

    const headers = inflate(columns, SEPARATOR)
    const rows = headers.length

    return (
      <thead>
        {
          headers.map((row, index) => (
            <tr key={index}>
              {
                (index === 0) &&
                <th rowSpan={rows} />
              }
              {
                (index === 0) &&
                <th rowSpan={rows}>
                  <FormattedMessage
                    id='response.list.table.created'
                    defaultMessage='Submitted' />
                </th>
              }

              {
                Object.keys(row).map(column => (
                  <th
                    key={row[column].key}
                    title={row[column].path}
                    rowSpan={row[column].isLeaf ? (rows - index) : 1}
                    colSpan={row[column].siblings}>
                    { row[column].label }
                  </th>
                ))
              }
            </tr>
          ))
        }
      </thead>
    )
  }

  renderResponse (response, index, columns) {
    const flattenData = flatten({...response.data}, SEPARATOR)

    return (
      <tr data-qa={`response-row-${response.id}`} key={response.id}>
        <td scope='row'>{this.props.start + index}</td>
        <td>
          <span className='mr-2'>
            <FormattedDate
              value={response.created}
              year='numeric'
              month='long'
              day='numeric' />
          </span>
          <span className='mr-2'>
            <FormattedTime
              value={response.created}
              hour12={false}
              hour='2-digit'
              minute='2-digit'
              second='2-digit'
              timeZoneName='short' />
          </span>
          <span>
            (<FormattedRelative value={response.created} />)
          </span>
        </td>

        {
          columns.map(key => (
            <td key={key}>
              <JSONViewer data={flattenData[key]} />
            </td>
          ))
        }
      </tr>
    )
  }
}
