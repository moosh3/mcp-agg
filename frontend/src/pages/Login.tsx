import React from 'react';
import { TextInput, PasswordInput, Button, Group, Box, Anchor } from '@mantine/core';
import { useForm } from '@mantine/form';
import { Link } from 'react-router-dom';
import { notifications } from '@mantine/notifications';

interface LoginProps {
  onLogin: (token: string) => void;
}

interface LoginFormValues {
  email: string;
  password: string;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const form = useForm<LoginFormValues>({
    initialValues: {
      email: '',
      password: '',
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value) => (value.length >= 6 ? null : 'Password must be at least 6 characters'),
    },
  });

  const handleSubmit = async (values: LoginFormValues) => {
    try {
      // In a real app, replace with actual API call
      const response = await fetch('/api/v1/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: values.email,
          password: values.password,
        }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      onLogin(data.access_token);
      
      notifications.show({
        title: 'Success',
        message: 'Logged in successfully',
        color: 'green',
      });
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Invalid credentials',
        color: 'red',
      });
      console.error('Login error:', error);
    }
  };

  return (
    <Box maw={400} mx="auto">
      <form onSubmit={form.onSubmit(handleSubmit)}>
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

        <Group justify="space-between" mt="md">
          <Anchor component={Link} to="/register" size="sm">
            Don't have an account? Register
          </Anchor>
          <Button type="submit">Login</Button>
        </Group>
      </form>
    </Box>
  );
};

export default Login;
