import React, { useState, useEffect } from 'react';
import { 
  Title, 
  Grid, 
  Card, 
  Text, 
  Button, 
  Group, 
  Loader, 
  Center, 
  Paper,
  Badge,
  ActionIcon
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
// Using Unicode symbols instead of icons library

interface AvailableApp {
  id: string;
  name: string;
  description: string;
  icon: string;
  auth_type: string;
}

interface UserApp {
  id: number;
  name: string;
  description: string;
  owner_id: number;
}

const Apps: React.FC = () => {
  const [availableApps, setAvailableApps] = useState<AvailableApp[]>([]);
  const [userApps, setUserApps] = useState<UserApp[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchApps = async () => {
    try {
      setLoading(true);
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
      const token = localStorage.getItem('token');

      if (!token) {
        throw new Error('Authentication required');
      }

      // Fetch available apps
      const availableAppsResponse = await fetch(`${apiBaseUrl}/apps`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!availableAppsResponse.ok) {
        throw new Error('Failed to fetch available apps');
      }

      // Fetch user's configured apps
      const userAppsResponse = await fetch(`${apiBaseUrl}/user/apps`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!userAppsResponse.ok) {
        throw new Error('Failed to fetch user apps');
      }

      const availableAppsData = await availableAppsResponse.json();
      const userAppsData = await userAppsResponse.json();

      setAvailableApps(availableAppsData);
      setUserApps(userAppsData);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching apps:', err);
      setError(err.message || 'Failed to load apps data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApps();
  }, []);

  const handleConfigureApp = (appId: string) => {
    // In a real implementation, this would redirect to an app-specific configuration page
    // or open a modal with configuration options
    notifications.show({
      title: 'Configuration',
      message: `Configure ${appId} integration. This would typically open a configuration modal or redirect to a configuration page.`,
      color: 'blue'
    });
  };

  const handleDeleteApp = async (appId: number) => {
    try {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
      const token = localStorage.getItem('token');

      const response = await fetch(`${apiBaseUrl}/user/apps/${appId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete app');
      }

      // Update the UI by removing the deleted app
      setUserApps(userApps.filter(app => app.id !== appId));

      notifications.show({
        title: 'Success',
        message: 'App integration removed successfully',
        color: 'green'
      });
    } catch (err: any) {
      console.error('Error deleting app:', err);
      notifications.show({
        title: 'Error',
        message: err.message || 'Failed to delete app',
        color: 'red'
      });
    }
  };

  // Helper function to check if app is configured
  const isAppConfigured = (appId: string) => {
    return userApps.some(app => app.name.toLowerCase() === appId.toLowerCase());
  };

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
        <Button mt="md" onClick={fetchApps}>
          🔄 Retry
        </Button>
      </Paper>
    );
  }

  return (
    <div>
      <Title order={2} mb="lg">Applications</Title>
      
      <Text mb="md">Available integrations you can configure:</Text>
      
      <Grid>
        {availableApps.map((app) => (
          <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={app.id}>
            <Card p="lg" radius="md" withBorder>
              <Group justify="space-between" mb="xs">
                <Text fw={500} size="lg">{app.name}</Text>
                {isAppConfigured(app.id) ? (
                  <Badge color="green">
                    ✓ Configured
                  </Badge>
                ) : null}
              </Group>
              
              <Text size="sm" c="dimmed" mb="md">{app.description}</Text>
              <Text size="xs" c="dimmed" mb="lg">Authentication: {app.auth_type}</Text>
              
              <Button 
                fullWidth 
                onClick={() => handleConfigureApp(app.id)}
                disabled={isAppConfigured(app.id)}
              >
                {isAppConfigured(app.id) ? 'Already Configured' : 'Configure'}
              </Button>
            </Card>
          </Grid.Col>
        ))}
      </Grid>

      {userApps.length > 0 && (
        <>
          <Title order={3} mt="xl" mb="md">Your Configured Apps</Title>
          
          <Grid>
            {userApps.map((app) => (
              <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={app.id}>
                <Card p="lg" radius="md" withBorder>
                  <Group justify="space-between">
                    <Text fw={500}>{app.name}</Text>
                    <ActionIcon color="red" onClick={() => handleDeleteApp(app.id)}>
                      🗑️
                    </ActionIcon>
                  </Group>
                  <Text size="sm" c="dimmed" mt="xs">{app.description || 'No description'}</Text>
                </Card>
              </Grid.Col>
            ))}
          </Grid>
        </>
      )}
    </div>
  );
};

export default Apps;
