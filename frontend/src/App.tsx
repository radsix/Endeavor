import { ChakraProvider } from '@chakra-ui/react'
import { defaultSystem } from "@chakra-ui/react"
import Header from "./components/headerENDHome";
import Customers from "./components/Customers";

function App() {

  return (
    <ChakraProvider value={defaultSystem}>
      <Header />
      <Customers /> {}
    </ChakraProvider>
  )
}

export default App;