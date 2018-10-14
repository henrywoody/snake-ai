import unittest
from mock import patch, MagicMock

from mixins import DrawableMixin


class MockDrawable(DrawableMixin):
	def __init__(self, position, size, color):
		self.position = position
		self.size = size
		self.color = color


class SnakeDrawTest(unittest.TestCase):
	def setUp(self):
		position = [1.95,8.23]
		size = 1
		color = (0,0,0)
		self.drawable = MockDrawable(position, size, color)

	@patch('pygame.draw.circle')
	def test_calls_pygame_draw_circle_with_the_correct_arguments(self, mock_draw_circle):
		'''DrawableMixin.draw calls pygame.draw.circle with information about the object's position (rounded) and size and color and the given surface object'''
		surface = MagicMock()
		self.drawable.draw(surface)

		expected_draw_position = [int(round(x)) for x in self.drawable.position]
		mock_draw_circle.assert_called_once_with(surface, self.drawable.color, expected_draw_position, self.drawable.size)


if __name__ == '__main__':
	unittest.main()