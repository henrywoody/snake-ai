import unittest
from mock import patch, call, MagicMock
import numpy as np

from snake import Snake
import utils


class MockObject:
	def __init__(self, position, size, visual_encoding=[1,1]):
		self.position = position
		self.size = size
		self.visual_encoding = visual_encoding


class SnakeUpdateTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	@patch.object(Snake, 'look', return_value=[5,6,100])
	@patch.object(Snake, 'decide', return_value=1)
	@patch.object(Snake, 'act')
	@patch.object(Snake, 'move')
	@patch.object(Snake, 'check_if_touching_tail')
	def test_calls_all_methods(self, mock_check_tail, mock_move, mock_act, mock_decide, mock_look):
		'''Snake.update calls look, decide, act, and move'''
		other_objects = [1,2,3]

		self.snake.update(other_objects)

		mock_look.assert_called_with(other_objects)
		mock_decide.assert_called_with(mock_look.return_value)
		mock_act.assert_called_with(mock_decide.return_value)
		self.assertTrue(mock_move.called)
		self.assertTrue(mock_check_tail.called)

class SnakeLookTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = np.pi/2
		self.snake = Snake(init_position, init_direction)
		self.snake.eye_angles = [0]

	def test_returns_zero_list_if_there_are_no_other_objects(self):
		'''Snake.look returns [0,0,0] for each eye if there is nothing to see'''
		self.snake.eye_angles = [0,1]
		other_objects = []
		output = self.snake.look(other_objects)

		expected_output = [0,0,0,0,0,0]
		self.assertListEqual(output, expected_output)

	def test_returns_zero_list_if_does_not_see_anything(self):
		'''Snake.look returns [0,0,0] for each eye if it does not see anything'''
		other_objects = [
			MockObject([2,2], 1),
			MockObject([0,-2], 1),
			MockObject([-2,2], 1),
			MockObject([2,-2], 1)
		]

		output = self.snake.look(other_objects)

		expected_output = [0,0,0]
		self.assertListEqual(output, expected_output)

	def test_returns_visual_encoding_of_object_it_sees(self):
		'''Snake.Eye.look returns the visual_encoding and distance of the object it sees'''
		expected_seen_object = MockObject([0,2], 1, visual_encoding=[2,2])
		other_objects = [
			expected_seen_object,
			MockObject([0,-2], 1, visual_encoding=[1,1])
		]

		output = self.snake.look(other_objects)

		expected_output = expected_seen_object.visual_encoding + [2]
		self.assertListEqual(output, expected_output)

	def test_returns_visual_encoding_of_closest_object_it_sees(self):
		'''Snake.Eye.look returns the visual_encoding and distance of the closest object it sees'''
		expected_seen_object = MockObject([0,2], 1, visual_encoding=[2,2])
		other_objects = [
			expected_seen_object,
			MockObject([0,5], 1, visual_encoding=[1,1]),
			MockObject([0,-2], 1, visual_encoding=[1,1])
		]

		output = self.snake.look(other_objects)

		expected_output = expected_seen_object.visual_encoding + [2]
		self.assertListEqual(output, expected_output)

	def test_can_see_an_object_if_angle_does_not_pass_through_center_but_passes_through_some_of_object(self):
		'''if the angle of the eye and the angle between the snake's head and the object are not equal but close enough (depending on obj size & distance) then the eye can see the object'''
		''' example: ( ) - object; x - snake;

			( )
			|
			|
			x
		'''
		expected_seen_object = MockObject([0.5,5], 1, visual_encoding=[1,1])
		other_objects = [
			expected_seen_object
		]

		output = self.snake.look(other_objects)

		snake_head = self.snake.body[0]
		expected_output = expected_seen_object.visual_encoding + [utils.calc_distance(snake_head.position, expected_seen_object.position)]
		self.assertListEqual(output, expected_output)

	def test_can_handle_an_object_with_distance_less_than_size(self):
		'''if the distance is less than the other_object's size, Snake.look does not throw an error'''
		other_objects = [
			MockObject([0,1], 5)
		]

		self.snake.look(other_objects)

	def test_can_see_body_pieces(self):
		'''Snake.look includes its own body pieces (not including first or second)'''
		self.snake.body.append(Snake.BodyPiece([0,0]))
		expected_seen_object = Snake.BodyPiece([0,10])
		self.snake.body.append(expected_seen_object)
		other_objects = []

		output = self.snake.look(other_objects)

		expected_output = expected_seen_object.visual_encoding + [10]
		self.assertListEqual(output, expected_output)


class SnakeDecideTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)

	@patch.object(Snake.Brain, 'forward')
	def test_passes_input_to_brain_to_forward(self, mock_forward):
		'''Snake.decide passes the input list as an array to Snake.Brain.forward'''
		information = [1,2,3,4]

		self.snake.decide(information)

		actual_input = mock_forward.call_args_list[0][0][0]
		expected_input = np.array(information)
		self.assertEqual(type(actual_input), np.ndarray)
		self.assertTrue(np.array_equal(actual_input, expected_input))

	@patch.object(Snake.Brain, 'forward', return_value=np.array([1,0,0]))
	def test_returns_argmax_of_output_from_brain_forward(self, mock_forward):
		'''Snake.decide returns the argmax of the output of Snake.Brain.forward'''
		information = [1,2,3,4]

		decision = self.snake.decide(information)

		expected_decision = mock_forward.return_value.argmax()
		self.assertEqual(decision, expected_decision)


class SnakeActTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		genome = [np.pi/5, np.pi/2]
		self.snake = Snake(init_position, init_direction, genome=genome)

	@patch.object(Snake, 'turn')
	def test_snake_does_a_negative_turn_angle1_turn_if_decision_is_0(self, mock_turn):
		'''if the decision is 0, the snake does negative turn_angle1 turn'''
		decision = 0

		self.snake.act(decision)

		mock_turn.assert_called_with(-self.snake.turn_angle1)

	@patch.object(Snake, 'turn')
	def test_snake_does_a_negative_turn_angle2_turn_if_decision_is_1(self, mock_turn):
		'''if the decision is 1, the snake does negative turn_angle2 turn'''
		decision = 1

		self.snake.act(decision)

		mock_turn.assert_called_with(-self.snake.turn_angle2)

	@patch.object(Snake, 'turn')
	def test_snake_does_a_positive_turn_angle1_turn_if_decision_is_2(self, mock_turn):
		'''if the decisionhis 2, the snake does positive turn_angle1 turn'''
		decision = 2

		self.snake.act(decision)

		mock_turn.assert_called_with(self.snake.turn_angle1)

	@patch.object(Snake, 'turn')
	def test_snake_does_positive_turn_angle2_turn_if_decision_is_3(self, mock_turn):
		'''if the decisionhis 3, the snake does positive turn_angle2 turn'''
		decision = 3

		self.snake.act(decision)

		mock_turn.assert_called_with(self.snake.turn_angle2)

	@patch.object(Snake, 'turn')
	def test_snake_does_nothing_if_decision_is_4(self, mock_turn):
		'''if the decisioniis index 4, the snake does nothing'''
		decision = 4

		self.snake.act(decision)

		self.assertFalse(mock_turn.called)


class SnakeGrowTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)
		self.snake.body[0].history = [[3,3], [2,2], [1,1], [0,0]]

	def test_adds_new_body_piece_at_correct_position_with_only_one_body_piece(self):
		'''Snake.grow adds a new body piece with position equal to the oldest position of the last body piece'''
		self.snake.grow()

		expected_length = 2
		self.assertEqual(len(self.snake.body), expected_length)
		expected_position = self.snake.body[-2].history[0]
		self.assertListEqual(self.snake.body[-1].position, expected_position)

	def test_adds_new_body_piece_at_correct_position_with_multiple_body_pieces(self):
		'''Snake.grow adds a new body piece with position equal to the oldest position of the last body piece'''
		last_piece = Snake.BodyPiece([1,1])
		last_piece.history = [[4,4], [3,3], [2,2], [1,1]]
		self.snake.body.append(last_piece)

		self.snake.grow()

		expected_length = 3
		self.assertEqual(len(self.snake.body), expected_length)
		expected_position = last_piece.history[0]
		self.assertListEqual(self.snake.body[-1].position, expected_position)

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


class SnakeCheckIfTouchingTailTest(unittest.TestCase):
	def setUp(self):
		init_position = [0,0]
		init_direction = 0
		self.snake = Snake(init_position, init_direction)
		for _ in range(5):
			self.snake.body.append(Snake.BodyPiece([0,0]))

	@patch('utils.are_touching', side_effect=[False, False, True, False])
	def test_snake_dies_if_head_is_touching_any_body_piece(self, mock_are_touching):
		'''Snake.check_if_touching_tail causes the snake to die if are_touching returns True for the head and any other body piece (except the second)'''
		self.snake.check_if_touching_tail()

		self.assertFalse(self.snake.is_alive)

	@patch('utils.are_touching', return_value=False)
	def test_snake_does_not_die_if_head_is_not_touching_any_body_piece(self, mock_are_touching):
		'''Snake.check_if_touching_tail does not cause the snake to die if are_touching returns False every time'''
		touching_tail = self.snake.check_if_touching_tail()

		self.assertTrue(self.snake.is_alive)


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






if __name__ == '__main__':
	unittest.main()