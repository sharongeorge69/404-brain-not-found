from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Generate a 5x5 maze
maze = [[random.choice([0, 1]) for _ in range(5)] for _ in range(5)]
start_position = {"x": 0, "y": 0}
goal_position = {"x": 4, "y": 4}
maze[start_position["x"]][start_position["y"]] = 0
maze[goal_position["x"]][goal_position["y"]] = 0
player_position = {"x": 0, "y": 0}


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    direction = data.get('direction')
    new_position = player_position.copy()

    if direction == 'up':
        new_position['x'] -= 1
    elif direction == 'down':
        new_position['x'] += 1
    elif direction == 'left':
        new_position['y'] -= 1
    elif direction == 'right':
        new_position['y'] += 1

    # Check bounds and wall collision
    if 0 <= new_position['x'] < 5 and 0 <= new_position['y'] < 5:
        if maze[new_position['x']][new_position['y']] == 0:
            player_position.update(new_position)
            near_goal = abs(goal_position['x'] - player_position['x']) + \
                abs(goal_position['y'] - player_position['y']) <= 1
            return jsonify(success=True, near_goal=near_goal, reached_goal=(player_position == goal_position))
        else:
            return jsonify(success=False, message="Hit a wall!")
    else:
        return jsonify(success=False, message="Out of bounds!")


if __name__ == "__main__":
    app.run(debug=True)
