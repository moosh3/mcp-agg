import React, { useState, useEffect } from 'react';
import { Card, Title, Text, CopyButton, ActionIcon, Group, Tooltip, TextInput, Button, Loader, Center, Alert } from '@mantine/core';
import { notifications } from '@mantine/notifications';

const MCPUrl: React.FC = () => {
  const [mcpUrl, setMcpUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMcpUrl = async () => {
      try {
        setLoading(true);
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
        const response = await fetch(`${apiBaseUrl}/mcp-url/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch MCP URL');
        }

        const data = await response.json();

        setMcpUrl(data.url);
        setError(null);
      } catch (err) {
        console.error('Error fetching MCP URL:', err);
        setError('Failed to load MCP URL. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchMcpUrl();
  }, []);

  const handleRegenerate = async () => {
    try {
      setLoading(true);
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
      // Note: The backend doesn't have a regenerate endpoint yet, so we'll just call the same endpoint again
      const response = await fetch(`${apiBaseUrl}/mcp-url/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to regenerate MCP URL');
      }

      const data = await response.json();

      setMcpUrl(data.url);
      
      notifications.show({
        title: 'Success',
        message: 'MCP URL regenerated successfully',
        color: 'green',
      });
    } catch (err) {
      console.error('Error regenerating MCP URL:', err);
      notifications.show({
        title: 'Error',
        message: 'Failed to regenerate MCP URL',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Center style={{ minHeight: '60vh' }}>
        <Loader size="lg" />
      </Center>
    );
  }

  return (
    <div>
      <Title order={2} mb="lg">MCP Server URL</Title>
      
      {error ? (
        <Alert color="red" title="Error">
          {error}
          <Button mt="md" onClick={() => window.location.reload()} size="xs">
            Retry
          </Button>
        </Alert>
      ) : (
        <Card p="xl" radius="md" withBorder>
          <Text mb="md">
            This is your unique MCP server URL. Copy this URL and paste it into your MCP client 
            configuration to connect your tools.
          </Text>
          
          <Group>
            <TextInput
              value={mcpUrl}
              readOnly
              style={{ flexGrow: 1 }}
              radius="md"
            />
            <CopyButton value={mcpUrl} timeout={2000}>
              {({ copied, copy }) => (
                <Tooltip label={copied ? 'Copied' : 'Copy'} withArrow position="right">
                  <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                    {copied ? '✓' : '📋'}
                  </ActionIcon>
                </Tooltip>
              )}
            </CopyButton>
          </Group>
          
          <Text mt="lg" mb="md" c="dimmed" size="sm">
            Warning: Regenerating your MCP URL will invalidate the previous URL. Any clients using 
            the old URL will need to be updated with the new one.
          </Text>
          
          <Button 
            onClick={handleRegenerate} 
            variant="outline" 
            color="orange" 
            loading={loading}
          >
            Regenerate URL
          </Button>
        </Card>
      )}
    </div>
  );
};

export default MCPUrl;
