import React, { useState, useEffect } from 'react';
import { Title, Card, Text, Group, Button, Switch, Loader, Center, Alert, Badge, Image, Table, ScrollArea, Divider } from '@mantine/core';
import { useParams, useNavigate } from 'react-router-dom';
import { notifications } from '@mantine/notifications';

interface Tool {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  requires_auth: boolean;
  capabilities: string[];
}

interface AppWithTools {
  id: string;
  name: string;
  description: string;
  logo: string;
  tools: Tool[];
}

const ToolsList: React.FC = () => {
  const { appId } = useParams<{ appId: string }>();
  const navigate = useNavigate();
  const [app, setApp] = useState<AppWithTools | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [enabledTools, setEnabledTools] = useState<{ [key: string]: boolean }>({});

  useEffect(() => {
    const fetchAppTools = async () => {
      try {
        setLoading(true);
        // In a real app, replace with actual API call
        const response = await fetch(`/api/v1/apps/${appId}/tools`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch tools for ${appId}`);
        }

        // For demo purposes - mock data
        // In a real app, use: const data = await response.json();
        let mockApp: AppWithTools;

        // Generate different mock data based on appId
        if (appId === 'github') {
          mockApp = {
            id: 'github',
            name: 'GitHub',
            description: 'Integrate with GitHub to access repositories, issues, and pull requests',
            logo: 'https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png',
            tools: [
              {
                id: 'github-repos',
                name: 'Repository Management',
                description: 'Create, list, and manage GitHub repositories',
                enabled: true,
                requires_auth: true,
                capabilities: ['List repositories', 'Create repositories', 'Manage branches']
              },
              {
                id: 'github-issues',
                name: 'Issue Tracking',
                description: 'Create, update, and track issues',
                enabled: true,
                requires_auth: true,
                capabilities: ['Create issues', 'Comment on issues', 'Manage labels']
              },
              {
                id: 'github-pr',
                name: 'Pull Requests',
                description: 'Manage pull requests and code reviews',
                enabled: true,
                requires_auth: true,
                capabilities: ['Create PRs', 'Review code', 'Merge PRs']
              },
              {
                id: 'github-actions',
                name: 'GitHub Actions',
                description: 'Run and manage GitHub Actions workflows',
                enabled: false,
                requires_auth: true,
                capabilities: ['List workflows', 'Trigger workflows', 'View run status']
              },
              {
                id: 'github-releases',
                name: 'Releases',
                description: 'Manage GitHub releases and tags',
                enabled: false,
                requires_auth: true,
                capabilities: ['Create releases', 'Upload assets', 'Manage tags']
              }
            ]
          };
        } else if (appId === 'slack') {
          mockApp = {
            id: 'slack',
            name: 'Slack',
            description: 'Connect to Slack workspaces to manage channels and messages',
            logo: 'https://a.slack-edge.com/80588/marketing/img/meta/slack_hash_128.png',
            tools: [
              {
                id: 'slack-messages',
                name: 'Messaging',
                description: 'Send and receive messages in channels and DMs',
                enabled: true,
                requires_auth: true,
                capabilities: ['Send messages', 'Read messages', 'React to messages']
              },
              {
                id: 'slack-channels',
                name: 'Channel Management',
                description: 'Create and manage Slack channels',
                enabled: true,
                requires_auth: true,
                capabilities: ['Create channels', 'Invite users', 'Manage topic']
              },
              {
                id: 'slack-files',
                name: 'File Sharing',
                description: 'Upload and manage files in Slack',
                enabled: false,
                requires_auth: true,
                capabilities: ['Upload files', 'Share files', 'Download files']
              },
              {
                id: 'slack-bots',
                name: 'Bot Interaction',
                description: 'Interact with other Slack bots',
                enabled: false,
                requires_auth: true,
                capabilities: ['Message bots', 'Use slash commands', 'Automate responses']
              }
            ]
          };
        } else {
          // Generic app template
          mockApp = {
            id: appId || 'unknown',
            name: appId ? appId.charAt(0).toUpperCase() + appId.slice(1) : 'Unknown App',
            description: 'Configure this application to use with MCP',
            logo: 'https://via.placeholder.com/128',
            tools: [
              {
                id: `${appId}-tool1`,
                name: 'Basic Functionality',
                description: 'Core features of the application',
                enabled: false,
                requires_auth: true,
                capabilities: ['Basic feature 1', 'Basic feature 2']
              },
              {
                id: `${appId}-tool2`,
                name: 'Advanced Functionality',
                description: 'Advanced features requiring additional permissions',
                enabled: false,
                requires_auth: true,
                capabilities: ['Advanced feature 1', 'Advanced feature 2']
              }
            ]
          };
        }

        setApp(mockApp);

        // Initialize enabled tools state
        const initialEnabledState: { [key: string]: boolean } = {};
        mockApp.tools.forEach(tool => {
          initialEnabledState[tool.id] = tool.enabled;
        });
        setEnabledTools(initialEnabledState);

        setError(null);
      } catch (err) {
        console.error(`Error fetching app tools:`, err);
        setError(`Failed to load tools for this application. Please try again.`);
      } finally {
        setLoading(false);
      }
    };

    if (appId) {
      fetchAppTools();
    }
  }, [appId]);

  const handleToolToggle = (toolId: string, enabled: boolean) => {
    setEnabledTools(prev => ({
      ...prev,
      [toolId]: enabled
    }));
  };

  const handleSaveTools = async () => {
    try {
      setSubmitting(true);
      // In a real app, replace with actual API call
      const response = await fetch(`/api/v1/apps/${appId}/tools`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tools: Object.entries(enabledTools).map(([id, enabled]) => ({
            id,
            enabled
          }))
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save tools configuration');
      }

      notifications.show({
        title: 'Success',
        message: `Tools for ${app?.name} saved successfully`,
        color: 'green',
      });
      
      // Update the app state to reflect changes
      if (app) {
        setApp({
          ...app,
          tools: app.tools.map(tool => ({
            ...tool,
            enabled: enabledTools[tool.id] || false
          }))
        });
      }
    } catch (err) {
      console.error('Error saving tool configuration:', err);
      notifications.show({
        title: 'Error',
        message: 'Failed to save tool configuration. Please try again.',
        color: 'red',
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Center style={{ minHeight: '60vh' }}>
        <Loader size="lg" />
      </Center>
    );
  }

  if (error || !app) {
    return (
      <Alert color="red" title="Error">
        {error || 'Application not found'}
        <Button mt="md" onClick={() => navigate('/apps')} size="xs">
          Back to Apps
        </Button>
      </Alert>
    );
  }

  // Calculate summary stats
  const totalTools = app.tools.length;
  const enabledToolsCount = Object.values(enabledTools).filter(Boolean).length;

  return (
    <div>
      <Group mb="lg">
        <Button variant="subtle" onClick={() => navigate('/apps')}>
          ← Back to Apps
        </Button>
      </Group>

      <Card p="xl" radius="md" withBorder mb="xl">
        <Group mb="md">
          <Image 
            src={app.logo} 
            h={50} 
            w={50} 
            fit="contain" 
            alt={`${app.name} logo`} 
          />
          <div>
            <Title order={2}>{app.name} Tools</Title>
            <Badge color="blue">
              {enabledToolsCount} of {totalTools} tools enabled
            </Badge>
          </div>
        </Group>

        <Text mb="lg">{app.description}</Text>
        
        <Text size="sm" fw={600} mt="xl" mb="md">
          Enable or disable tools to customize your MCP experience
        </Text>

        <ScrollArea h={400} offsetScrollbars>
          <Table highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Tool</Table.Th>
                <Table.Th>Description</Table.Th>
                <Table.Th>Capabilities</Table.Th>
                <Table.Th style={{ width: 120, textAlign: 'center' }}>Status</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {app.tools.map((tool) => (
                <Table.Tr key={tool.id}>
                  <Table.Td>
                    <Text fw={600}>{tool.name}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm">{tool.description}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm">
                      {tool.capabilities.map((cap, idx) => (
                        <Badge key={idx} variant="light" radius="sm" mr="xs" mb="xs">
                          {cap}
                        </Badge>
                      ))}
                    </Text>
                  </Table.Td>
                  <Table.Td style={{ textAlign: 'center' }}>
                    <Switch 
                      checked={enabledTools[tool.id] || false}
                      onChange={(event) => handleToolToggle(tool.id, event.currentTarget.checked)}
                      size="md"
                    />
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </ScrollArea>

        <Divider my="lg" />

        <Group justify="flex-end" mt="md">
          <Button 
            variant="outline" 
            onClick={() => navigate(`/apps/${appId}/config`)}
          >
            Edit Configuration
          </Button>
          <Button 
            onClick={handleSaveTools} 
            loading={submitting}
          >
            Save Tool Settings
          </Button>
        </Group>
      </Card>
    </div>
  );
};

export default ToolsList;
