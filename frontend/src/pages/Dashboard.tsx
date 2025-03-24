import React, { useState, useEffect } from 'react';
import { Card, SimpleGrid, Title, Text, Button, Group, Loader, Center, Paper } from '@mantine/core';
import { Link } from 'react-router-dom';

interface AppStats {
  totalApps: number;
  configuredApps: number;
  totalTools: number;
  enabledTools: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<AppStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        // Call the dashboard stats API we just implemented
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
        const response = await fetch(`${apiBaseUrl}/dashboard/stats`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch dashboard stats');
        }
        
        const data = await response.json();

        setStats(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching stats:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const StatCard = ({ title, value, description, linkTo, linkText }: 
    { title: string; value: number; description: string; linkTo: string; linkText: string }) => (
    <Card p="xl" radius="md" withBorder>
      <Title order={3}>{title}</Title>
      <Text my="md" fw={700} size="xl">{value}</Text>
      <Text mb="md" c="dimmed" size="sm">{description}</Text>
      <Button component={Link} to={linkTo} variant="light" fullWidth>{linkText}</Button>
    </Card>
  );

  if (loading) {
    return (
      <Center style={{ minHeight: '60vh' }}>
        <Loader size="lg" />
      </Center>
    );
  }

  if (error) {
    return (
      <Paper p="xl" withBorder>
        <Text c="red">{error}</Text>
        <Button mt="md" onClick={() => window.location.reload()}>Retry</Button>
      </Paper>
    );
  }

  return (
    <div>
      <Title order={2} mb="lg">Dashboard</Title>
      
      <SimpleGrid cols={{ base: 1, xs: 2, md: 4 }}>
        <StatCard 
          title="Total Apps" 
          value={stats?.totalApps || 0} 
          description="Number of apps available" 
          linkTo="/apps" 
          linkText="Browse Apps" 
        />
        <StatCard 
          title="Configured Apps" 
          value={stats?.configuredApps || 0} 
          description="Apps with connection details" 
          linkTo="/apps" 
          linkText="Configure Apps" 
        />
        <StatCard 
          title="Total Tools" 
          value={stats?.totalTools || 0} 
          description="Available tools across all apps" 
          linkTo="/apps" 
          linkText="View Tools" 
        />
        <StatCard 
          title="Enabled Tools" 
          value={stats?.enabledTools || 0} 
          description="Tools currently enabled" 
          linkTo="/apps" 
          linkText="Manage Tools" 
        />
      </SimpleGrid>
      
      <Group mt="xl">
        <Button component={Link} to="/mcp-url" size="md">
          View MCP Server URL
        </Button>
        <Button component={Link} to="/apps" size="md" variant="outline">
          Configure Applications
        </Button>
      </Group>
    </div>
  );
};

export default Dashboard;
