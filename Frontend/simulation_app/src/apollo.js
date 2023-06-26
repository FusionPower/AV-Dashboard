import { ApolloClient, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:5000/graphql', // update this to your GraphQL server URI
  cache: new InMemoryCache()
});

export default client;