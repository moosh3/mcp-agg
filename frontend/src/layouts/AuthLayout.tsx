import React from 'react';
import { Outlet } from 'react-router-dom';
import { Container, Paper, Title, Text, Box } from '@mantine/core';

const AuthLayout: React.FC = () => {
  return (
    <Container size="sm" p="xl" style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Paper radius="md" p="xl" withBorder style={{ width: '100%', maxWidth: 450 }}>
        <Box mb="lg" style={{ textAlign: 'center' }}>
          <Title order={2} mb="xs">MCP Aggregator</Title>
          <Text c="dimmed" size="sm">Access all your tools in one place</Text>
        </Box>
        <Outlet />
      </Paper>
    </Container>
  );
};

export default AuthLayout;
