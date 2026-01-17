import unittest
from src.mcp_server import MCPServer

class TestMCPServer(unittest.TestCase):
    def test_mcp_server_initialization(self):
        server = MCPServer()

        # Check that all handlers are registered
        self.assertTrue(hasattr(server, 'image_handler'))
        self.assertTrue(hasattr(server, 'text_handler'))
        self.assertTrue(hasattr(server, 'audio_handler'))

        # Check that server can start
        self.assertTrue(server.start())

if __name__ == '__main__':
    unittest.main()