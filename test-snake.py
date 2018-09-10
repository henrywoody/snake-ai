import unittest
from mock import patch, call, MagicMock
import numpy as np

from snake import Snake


class SnakeBodyPieceMoveToTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		self.body_piece = Snake.BodyPiece(init_position)

	def test_moves_body_piece_to_new_position(self):
		'''Snake.BodyPiece.move_to moves the body_piece piece to the given position'''
		init_position = [0,0]
		expected_position = [1,1]
		
		self.body_piece.move_to(expected_position)

		self.assertListEqual(self.body_piece.position, expected_position)

	@patch.object(Snake.BodyPiece, 'update_history')
	def test_calls_update_history_with_new_position(self, mock_update_history):
		'''Snake.Head.move calls update_history with the new position'''
		init_position = [0,0]
		expected_position = [1,1]
		
		self.body_piece.move_to(expected_position)

		expected_calls = [call(expected_position)]
		mock_update_history.assert_has_calls(expected_calls)

class SnakeBodyPieceUpdateHistoryTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		self.body_piece = Snake.BodyPiece(init_position)

	def test_appends_new_position_to_history(self):
		'''when given a new value BodyPiece.update_history appends the new position to the end of the BodyPiece's history'''
		expected_position = [1,2]
		self.body_piece.history = [[0,0], [1,1]]
		
		self.body_piece.update_history(expected_position)

		self.assertListEqual(self.body_piece.history[-1], expected_position)

	def test_trims_history_if_necessary(self):
		'''if the length of the BodyPiece's history is greater than max_history, update_history trims the history by removing from the front'''
		self.body_piece.max_history = 3
		expected_position = [1,2]
		init_history = [[0,0], [1,1], [2,1], [2,2], [1,1]]
		self.body_piece.history = init_history[:]
		
		self.body_piece.update_history(expected_position)

		self.assertListEqual(self.body_piece.history, init_history[3:] + [expected_position])

	def test_does_not_trim_history_if_not_necessary(self):
		'''if the length of the BodyPiece's history is less than or equal to max_history, update_history does not trim the history'''
		self.body_piece.max_history = 5
		expected_position = [1,2]
		init_history = [[0,0], [1,1], [2,1], [2,2]]
		self.body_piece.history = init_history[:]
		
		self.body_piece.update_history(expected_position)

		self.assertListEqual(self.body_piece.history, init_history + [expected_position])


class SnakeBodyPieceDrawTest(unittest.TestCase):
	def setUp(self):
		init_position = [0.1,0.9]
		self.body_piece = Snake.BodyPiece(init_position)

	@patch('pygame.draw.circle')
	def test_calls_pygame_draw_circle_with_the_correct_arguments(self, mock_draw_circle):
		'''Snake.BodyPiece.draw calls pygame.draw.circle with information about the piece's position (rounded) and size and color and the given surface object'''
		surface = MagicMock()
		self.body_piece.draw(surface)

		draw_position = [int(round(x)) for x in self.body_piece.position]
		mock_draw_circle.assert_called_once_with(surface, self.body_piece.color, draw_position, self.body_piece.size)


class SnakeTurnTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	def test_adds_given_angle_to_direction_mod_2pi(self):
		'''Snake.turn takes an angle and adds it to its direction (mod 2*pi)'''
		directions		= [0,			3*np.pi/2,	np.pi/4,	3*np.pi/4]
		turn_angles		= [np.pi/2,		np.pi,		-np.pi/2,	np.pi/2]
		final_direction	= [np.pi/2,		np.pi/2,	7*np.pi/4,	5*np.pi/4]
		for direction, turn_angle, expected_direction in zip(directions, turn_angles, final_direction):
			self.snake.direction = direction

			self.snake.turn(turn_angle)

			self.assertEqual(self.snake.direction, expected_direction)


class SnakeMoveTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	@patch.object(Snake, 'calc_next_position', return_value=[5,5])
	@patch.object(Snake.BodyPiece, 'move_to')
	def test_moves_the_first_body_piece_to_next_position(self, mock_move_to, mock_calc_next_position):
		'''Snake.move calls calc_next_position and moves the first body_piece to that position'''
		expected_position = mock_calc_next_position.return_value
		self.snake.move()

		expected_calls = [call(expected_position)]
		mock_move_to.assert_has_calls(expected_calls)

	@patch.object(Snake.BodyPiece, 'move_to')
	def test_calls_move_to_on_all_tail_pieces_with_correct_positions(self, mock_move_to):
		'''Snake.move calls Snake.BodyPiece.move_to on each but the first of the snake's body_pieces with the oldest position in the preceeding body piece's history'''
		self.snake.body = []
		histories = [
			[[1,1], [1,2], [1,3], [1,4], [1,5]],
			[[1,2], [1,3], [1,4], [1,5], [1,6]],
			[[1,3], [1,4], [1,5], [1,6], [1,7]],
			[[1,4], [1,5], [1,6], [1,7], [1,8]],
		]
		for history in histories:
			new_piece = Snake.BodyPiece(history[-1][:])
			new_piece.history = history[:]
			self.snake.body.append(new_piece)

		self.snake.move()

		expected_calls = [call(history[0]) for history in histories[:-1]]
		mock_move_to.assert_has_calls(expected_calls)


class SnakeCalcNextPositionTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	def test_calculates_next_position_according_to_speed_and_direction(self):
		'''Snake.calc_next_position calculates the next positiion according to its speed and direction'''
		directions = [0, np.pi/2, np.pi, 10*np.pi/6, -np.pi/3, 1, 3]
		for direction in directions:
			self.snake.direction = direction
			head_piece = self.snake.body[0]
			expected_x = head_piece.position[0] + self.snake.speed * np.cos(self.snake.direction)
			expected_y = head_piece.position[1] + self.snake.speed * np.sin(self.snake.direction)
			
			next_position = self.snake.calc_next_position()

			self.assertListEqual(next_position, [expected_x, expected_y])


class SnakeDrawTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	@patch.object(Snake.BodyPiece, 'draw')
	def test_calls_pygame_draw_circle_with_the_correct_arguments(self, mock_draw):
		'''Snake.draw calls draw on each of its body_pieces, passing the given surface along'''
		self.snake.body = [Snake.BodyPiece([0,0]) for _ in range(5)]
		surface = MagicMock()
		self.snake.draw(surface)

		expected_calls = [call(surface) for _ in range(5)]
		mock_draw.assert_has_calls(expected_calls)




if __name__ == '__main__':
	unittest.main()