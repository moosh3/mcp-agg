import React, { useState, useEffect } from 'react';
import { Title, Card, SimpleGrid, Text, Badge, Group, Button, Image, Loader, Center, Alert } from '@mantine/core';
import { Link } from 'react-router-dom';

interface App {
  id: string;
  name: string;
  description: string;
  logo: string;
  isConfigured: boolean;
  toolsCount: number;
  enabledToolsCount: number;
}

const AppsList: React.FC = () => {
  const [apps, setApps] = useState<App[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        setLoading(true);
        // In a real app, replace with actual API call
        const response = await fetch('/api/v1/apps', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch apps');
        }

        // For demo purposes - mock data
        // In a real app, use: const data = await response.json();
        const mockApps = [
          {
            id: 'github',
            name: 'GitHub',
            description: 'Integrate with GitHub to access repositories, issues, and pull requests',
            logo: 'https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png',
            isConfigured: true,
            toolsCount: 5,
            enabledToolsCount: 3
          },
          {
            id: 'slack',
            name: 'Slack',
            description: 'Connect to Slack workspaces to manage channels and messages',
            logo: 'https://a.slack-edge.com/80588/marketing/img/meta/slack_hash_128.png',
            isConfigured: true,
            toolsCount: 4,
            enabledToolsCount: 2
          },
          {
            id: 'jira',
            name: 'Jira',
            description: 'Work with Jira issues, projects, and boards',
            logo: 'https://wac-cdn.atlassian.com/assets/img/favicons/atlassian/favicon-32x32.png',
            isConfigured: false,
            toolsCount: 3,
            enabledToolsCount: 0
          },
          {
            id: 'gmail',
            name: 'Gmail',
            description: 'Access and manage emails and drafts in Gmail',
            logo: 'https://ssl.gstatic.com/ui/v1/icons/mail/rfr/gmail.ico',
            isConfigured: false,
            toolsCount: 2,
            enabledToolsCount: 0
          },
          {
            id: 'google-drive',
            name: 'Google Drive',
            description: 'Work with files and folders in Google Drive',
            logo: 'https://ssl.gstatic.com/images/branding/product/1x/drive_2020q4_32dp.png',
            isConfigured: true,
            toolsCount: 3,
            enabledToolsCount: 3
          }
        ];

        setApps(mockApps);
        setError(null);
      } catch (err) {
        console.error('Error fetching apps:', err);
        setError('Failed to load applications. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchApps();
  }, []);

  if (loading) {
    return (
      <Center style={{ minHeight: '60vh' }}>
        <Loader size="lg" />
      </Center>
    );
  }

  if (error) {
    return (
      <Alert color="red" title="Error">
        {error}
        <Button mt="md" onClick={() => window.location.reload()} size="xs">
          Retry
        </Button>
      </Alert>
    );
  }

  return (
    <div>
      <Title order={2} mb="lg">Available Applications</Title>
      <Text mb="xl" c="dimmed">
        Configure these applications to use their tools with MCP. You'll need to provide
        connection information and select which tools to enable.
      </Text>
      
      <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="lg">
        {apps.map((app) => (
          <Card key={app.id} p="lg" radius="md" withBorder>
            <Card.Section p="md">
              <Group>
                <Image 
                  src={app.logo} 
                  h={40} 
                  w={40} 
                  fit="contain" 
                  alt={`${app.name} logo`} 
                />
                <div>
                  <Text fw={500} size="lg">{app.name}</Text>
                  <Badge color={app.isConfigured ? 'teal' : 'gray'}>
                    {app.isConfigured ? 'Configured' : 'Not Configured'}
                  </Badge>
                </div>
              </Group>
            </Card.Section>
            
            <Text mt="sm" mb="md" size="sm">
              {app.description}
            </Text>
            
            <Text size="xs" c="dimmed" mb="md">
              {app.enabledToolsCount} of {app.toolsCount} tools enabled
            </Text>
            
            <Group>
              <Button 
                component={Link} 
                to={`/apps/${app.id}/config`} 
                variant={app.isConfigured ? "light" : "filled"}
                fullWidth
              >
                {app.isConfigured ? 'Edit Configuration' : 'Configure'}
              </Button>
              
              {app.isConfigured && (
                <Button 
                  component={Link} 
                  to={`/apps/${app.id}/tools`} 
                  variant="outline"
                  fullWidth
                >
                  Manage Tools
                </Button>
              )}
            </Group>
          </Card>
        ))}
      </SimpleGrid>
    </div>
  );
};

export default AppsList;
