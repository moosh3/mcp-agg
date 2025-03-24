import React from 'react';
import { TextInput, PasswordInput, Button, Group, Box, Anchor } from '@mantine/core';
import { useForm } from '@mantine/form';
import { Link } from 'react-router-dom';
import { notifications } from '@mantine/notifications';

interface RegisterProps {
  onRegister: (token: string) => void;
}

interface RegisterFormValues {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const Register: React.FC<RegisterProps> = ({ onRegister }) => {
  const form = useForm<RegisterFormValues>({
    initialValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validate: {
      name: (value) => (value.length > 0 ? null : 'Name is required'),
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value) => (value.length >= 6 ? null : 'Password must be at least 6 characters'),
      confirmPassword: (value, values) => 
        value === values.password ? null : 'Passwords do not match',
    },
  });

  const handleSubmit = async (values: RegisterFormValues) => {
    try {
      // Use direct fetch calls to communicate with the backend API

      // Register the user using the correct endpoint as per the API implementation
      // The endpoint should be /api/v1/register according to the backend code
      await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: values.email,
          password: values.password,
        }),
      });
      
      // After successful registration, log in the user via the token endpoint
      // The endpoint should be /api/v1/token according to the backend code
      const loginResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: values.email,
          password: values.password,
        }),
      });
      
      if (!loginResponse.ok) {
        throw new Error('Login after registration failed');
      }
      
      const data = await loginResponse.json();

      // Set the token in localStorage
      const token = data.access_token;
      localStorage.setItem('token', token);
      
      // Call the onRegister callback with the token
      onRegister(token);
      
      notifications.show({
        title: 'Success',
        message: 'Account created successfully',
        color: 'green',
      });
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Registration failed. Please try again.',
        color: 'red',
      });
      console.error('Registration error:', error);
    }
  };

  return (
    <Box maw={400} mx="auto">
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <TextInput
          withAsterisk
          label="Name"
          placeholder="Your name"
          {...form.getInputProps('name')}
          mb="md"
        />
        
        <TextInput
          withAsterisk
          label="Email"
          placeholder="your@email.com"
          {...form.getInputProps('email')}
          mb="md"
        />
        
        <PasswordInput
          withAsterisk
          label="Password"
          placeholder="Your password"
          {...form.getInputProps('password')}
          mb="md"
        />
        
        <PasswordInput
          withAsterisk
          label="Confirm Password"
          placeholder="Confirm your password"
          {...form.getInputProps('confirmPassword')}
          mb="md"
        />

        <Group justify="space-between" mt="md">
          <Anchor component={Link} to="/login" size="sm">
            Already have an account? Login
          </Anchor>
          <Button type="submit">Register</Button>
        </Group>
      </form>
    </Box>
  );
};

export default Register;
