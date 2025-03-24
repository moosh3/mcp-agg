import React, { useState, useEffect } from 'react';
import { Title, Card, Text, Group, Button, TextInput, PasswordInput, Switch, Divider, Loader, Center, Alert, Badge, Image } from '@mantine/core';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';

interface AppDetails {
  id: string;
  name: string;
  description: string;
  logo: string;
  isConfigured: boolean;
  configFields: {
    name: string;
    key: string;
    type: 'text' | 'password' | 'boolean';
    required: boolean;
    description: string;
    value?: string | boolean;
  }[];
}

const AppConfig: React.FC = () => {
  const { appId } = useParams<{ appId: string }>();
  const navigate = useNavigate();
  const [app, setApp] = useState<AppDetails | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize form with empty values that will be updated later
  const form = useForm<Record<string, any>>({
    initialValues: {},
    validate: {},
  });

  useEffect(() => {
    const fetchAppDetails = async () => {
      try {
        setLoading(true);
        // In a real app, replace with actual API call
        const response = await fetch(`/api/v1/apps/${appId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch app details for ${appId}`);
        }

        // For demo purposes - mock data
        // In a real app, use: const data = await response.json();
        let mockApp: AppDetails;

        // Generate different mock data based on appId
        if (appId === 'github') {
          mockApp = {
            id: 'github',
            name: 'GitHub',
            description: 'Integrate with GitHub to access repositories, issues, and pull requests',
            logo: 'https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png',
            isConfigured: true,
            configFields: [
              {
                name: 'Personal Access Token',
                key: 'access_token',
                type: 'password',
                required: true,
                description: 'GitHub personal access token with repo and user permissions',
                value: '•••••••••••••••••••',
              },
              {
                name: 'Default Repository',
                key: 'default_repo',
                type: 'text',
                required: false,
                description: 'Optional: Default repository to use (format: owner/repo)',
                value: 'moosh3/mcp-agg',
              },
              {
                name: 'Enable Notifications',
                key: 'enable_notifications',
                type: 'boolean',
                required: false,
                description: 'Receive notifications for GitHub events',
                value: true,
              },
            ],
          };
        } else if (appId === 'slack') {
          mockApp = {
            id: 'slack',
            name: 'Slack',
            description: 'Connect to Slack workspaces to manage channels and messages',
            logo: 'https://a.slack-edge.com/80588/marketing/img/meta/slack_hash_128.png',
            isConfigured: true,
            configFields: [
              {
                name: 'Bot Token',
                key: 'bot_token',
                type: 'password',
                required: true,
                description: 'Slack bot token (starts with xoxb-)',
                value: '•••••••••••••••••••',
              },
              {
                name: 'Default Channel',
                key: 'default_channel',
                type: 'text',
                required: false,
                description: 'Optional: Default channel for messages',
                value: 'general',
              },
            ],
          };
        } else {
          // Generic app template
          mockApp = {
            id: appId || 'unknown',
            name: appId ? appId.charAt(0).toUpperCase() + appId.slice(1) : 'Unknown App',
            description: 'Configure this application to use with MCP',
            logo: 'https://via.placeholder.com/128',
            isConfigured: false,
            configFields: [
              {
                name: 'API Key',
                key: 'api_key',
                type: 'password',
                required: true,
                description: 'API key for authentication',
                value: '',
              },
              {
                name: 'API URL',
                key: 'api_url',
                type: 'text',
                required: false,
                description: 'API endpoint URL (if different from default)',
                value: '',
              },
            ],
          };
        }

        setApp(mockApp);

        // Initialize form with values from app
        const initialValues: Record<string, any> = {};
        const validationRules: Record<string, any> = {};

        mockApp.configFields.forEach((field) => {
          initialValues[field.key] = field.value || (field.type === 'boolean' ? false : '');
          
          if (field.required && field.type !== 'boolean') {
            validationRules[field.key] = (value: string) => 
              (!value || value.trim() === '') ? `${field.name} is required` : null;
          }
        });

        form.setValues(initialValues);
        // Set form validation manually since we can't use setValidate directly
        form.clearErrors();
        // We'll manually check validation during the handleSubmit function

        setError(null);
      } catch (err) {
        console.error(`Error fetching app details:`, err);
        setError(`Failed to load application details. Please try again.`);
      } finally {
        setLoading(false);
      }
    };

    if (appId) {
      fetchAppDetails();
    }
  }, [appId]);

  const handleSubmit = async (values: Record<string, any>) => {
    try {
      setSubmitting(true);
      // In a real app, replace with actual API call
      const response = await fetch(`/api/v1/apps/${appId}/config`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error('Failed to save app configuration');
      }

      notifications.show({
        title: 'Success',
        message: `${app?.name} configuration saved successfully`,
        color: 'green',
      });

      // Navigate to tools configuration page
      navigate(`/apps/${appId}/tools`);
    } catch (err) {
      console.error('Error saving app config:', err);
      notifications.show({
        title: 'Error',
        message: 'Failed to save configuration. Please try again.',
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
            <Title order={2}>{app.name} Configuration</Title>
            <Badge color={app.isConfigured ? 'teal' : 'gray'}>
              {app.isConfigured ? 'Currently Configured' : 'Not Yet Configured'}
            </Badge>
          </div>
        </Group>

        <Text mb="lg">{app.description}</Text>
        
        <Divider my="lg" />

        <form onSubmit={form.onSubmit(handleSubmit)}>
          {app.configFields.map((field) => (
            <div key={field.key} style={{ marginBottom: '1rem' }}>
              {field.type === 'password' ? (
                <PasswordInput
                  label={field.name}
                  placeholder={`Enter ${field.name.toLowerCase()}`}
                  description={field.description}
                  required={field.required}
                  mb="md"
                  {...form.getInputProps(field.key)}
                />
              ) : field.type === 'text' ? (
                <TextInput
                  label={field.name}
                  placeholder={`Enter ${field.name.toLowerCase()}`}
                  description={field.description}
                  required={field.required}
                  mb="md"
                  {...form.getInputProps(field.key)}
                />
              ) : (
                <Switch
                  label={field.name}
                  description={field.description}
                  mb="md"
                  {...form.getInputProps(field.key, { type: 'checkbox' })}
                />
              )}
            </div>
          ))}

          <Group justify="flex-end" mt="xl">
            <Button type="button" variant="subtle" onClick={() => navigate('/apps')}>
              Cancel
            </Button>
            <Button type="submit" loading={submitting}>
              Save Configuration
            </Button>
          </Group>
        </form>
      </Card>
    </div>
  );
};

export default AppConfig;
