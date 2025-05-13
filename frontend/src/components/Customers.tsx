import React, { useEffect, useState, createContext, useContext } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

// Define the new data structure based on the response
interface Customer {
  city: string;
  name: string;
  country: string;
  contact: string;
  phone: string;
  comments: string;
  address1: string;
  address2: string;
  UUID: string;
  state: string;
  zip: string;
  contactPosition: string;
  email: string;
}

const CustomersContext = createContext({
  customers: [] as Customer[], // Updated context type
  fetchCustomers: () => {} // Fetch function for customers
});

function AddCustomer() {
  const [newCustomer, setNewCustomer] = useState<Customer>({
    city: "",
    name: "",
    country: "",
    contact: "",
    phone: "",
    comments: "",
    address1: "",
    address2: "",
    UUID: "",
    state: "",
    zip: "",
    contactPosition: "",
    email: "",
  });

  const { fetchCustomers } = React.useContext(CustomersContext);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNewCustomer((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    fetch("http://localhost:8000/customer/createCustomer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newCustomer),
    }).then(() => fetchCustomers());
  };

  return (
    <form onSubmit={handleSubmit}>
      {Object.keys(newCustomer).map((key) => (
        key !== "UUID" && (  // Exclude UUID field, assuming it's auto-generated
          <div key={key}>
            <Input
              name={key}
              value={(newCustomer as any)[key]}
              onChange={handleInputChange}
              placeholder={`Enter ${key}`}
              aria-label={key}
              mb={3}
            />
          </div>
        )
      ))}
      <Button type="submit">Add Customer</Button>
    </form>
  );
}

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]); // Updated state type
  const fetchCustomers = async () => {
    const response = await fetch("http://localhost:8000/customer/getCustomers");
    const data = await response.json();
    setCustomers(data); // Directly set the array
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  return (
    <CustomersContext.Provider value={{ customers, fetchCustomers }}>
      <Container maxW="container.xl" pt="100px">
        <AddCustomer />
        <Stack gap={5}>
          {customers.map((customer: Customer) => (
            <Box key={customer.UUID} border="1px" p="4" borderRadius="md">
              <Text><b>Name:</b> {customer.name}</Text>
              <Text><b>Phone:</b> {customer.phone}</Text>
              <Text><b>Email:</b> {customer.email}</Text>
              <Text><b>Address:</b> {customer.address1}, {customer.address2}, {customer.city}, {customer.state}, {customer.country}, {customer.zip}</Text>
              <Text><b>Comments:</b> {customer.comments}</Text>
              <Text><b>Contact:</b> {customer.contact}, {customer.contactPosition}</Text>
            </Box>
          ))}
        </Stack>
      </Container>
    </CustomersContext.Provider>
  );
}