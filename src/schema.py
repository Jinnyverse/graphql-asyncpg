from graphql import build_schema
import resolvers

schema = build_schema("""
  type Mutation {
    insertThousand(id: Int): String
  }

  type Query {
    hello: String
    getAll: [User]!
  }

  type User {
    id: Int
    email: Int
    company: Int
  }
""")

fields = schema.mutation_type.fields
fields["insertThousand"].resolve = resolvers.insert_thousand

fields = schema.query_type.fields
fields["getAll"].resolve = resolvers.get_all

fields = schema.get_type('User').fields
