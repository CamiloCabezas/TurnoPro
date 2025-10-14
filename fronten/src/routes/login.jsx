import { VStack, FormControl, FormLabel, Input, Button } from "@chakra-ui/react";
import {  useState } from "react";
import { login } from "../endpoints/api";

export default function Login() {

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = async () => {
    login(username, password)
    
  }

  return (
    <VStack spacing={4}>
      <FormControl>
        <FormLabel>Email</FormLabel>
        <Input onChange={(e) => setUsername(e.target.value)} value={username} type="text" />
      </FormControl>


      <FormControl>
        <FormLabel>Password</FormLabel>
        <Input onChange={(e) => setPassword(e.target.value)} value={password} type="password" />
      </FormControl>

      <Button colorScheme="teal" onClick={handleLogin}>
        Login
      </Button>
    </VStack>
  );
}
