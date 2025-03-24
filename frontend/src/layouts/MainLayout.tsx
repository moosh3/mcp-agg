import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { AppShell, Button, Group, Text, NavLink, Box, Flex, Burger, ScrollArea } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

interface MainLayoutProps {
  onLogout: () => void;
  isAuthenticated: boolean;
}

const MainLayout: React.FC<MainLayoutProps> = ({ onLogout, isAuthenticated }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [opened, { toggle }] = useDisclosure();

  // Redirect to login if not authenticated
  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: '📊' },
    { label: 'MCP URL', path: '/mcp-url', icon: '🔗' },
    { label: 'Configure Apps', path: '/apps', icon: '⚙️' },
  ];

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{ width: 300, breakpoint: 'sm', collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header>
        <Flex h="100%" px="md" align="center" justify="space-between">
          <Group>
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <Text fw={700} size="lg">MCP Aggregator</Text>
          </Group>
          <Button color="red" onClick={handleLogout} variant="subtle">Logout</Button>
        </Flex>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <AppShell.Section grow component={ScrollArea}>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              label={item.label}
              leftSection={<Text>{item.icon}</Text>}
              active={location.pathname === item.path}
              component={Link}
              to={item.path}
              variant="filled"
              mb="xs"
            />
          ))}
        </AppShell.Section>
        
        <AppShell.Section>  
          <Box mt="xl" pt="md" style={{ borderTop: '1px solid #eaeaea' }}>
            <Text size="xs" c="dimmed" ta="center" py="md">
              MCP Aggregator v1.0.0
            </Text>
          </Box>
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
};

export default MainLayout;
