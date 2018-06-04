const entityTypes = [
  {
    'type': 'record',
    'name': 'Person',
    'fields': [
      {
        'name': 'hatId',
        'type': 'string'
      },
      {
        'name': 'firstName',
        'type': 'string'
      },
      {
        'name': 'lastName',
        'type': 'string'
      },
      {
        'name': 'age',
        'type': 'int'
      },
      {
        'name': 'gender',
        'type': {
          'type': 'enum',
          'name': 'Gender',
          'symbols': [ 'MALE', 'FEMALE' ]
        }
      }
    ]
  },
  {
    'type': 'record',
    'name': 'Screening',
    'fields': [
      {
        'name': 'hatId',
        'type': 'string'
      },
      {
        'name': 'screening',
        'type': {
          'type': 'enum',
          'name': 'ScreeningType',
          'symbols': [ 'maect', 'catt', 'pg', 'ctcwoo', 'ge', 'pl' ]
        }
      },
      {
        'name': 'location',
        'type': {
          'type': 'record',
          'name': 'GeoLocation',
          'fields': [
            {
              'name': 'latitude',
              'type': 'float'
            },
            {
              'name': 'longitude',
              'type': 'float'
            }
          ]
        }
      },
      {
        'name': 'result',
        'type': {
          'type': 'enum',
          'name': 'Result',
          'symbols': [ 'positive', 'negative' ]
        }
      }
    ]
  }
]

export default entityTypes
