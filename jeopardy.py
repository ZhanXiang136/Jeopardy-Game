import requests
import pandas as pd
import os 
import time

def start_up():
    points = [500, 400, 300, 200, 100]
    game_board_dict = {}
    game_info = {}

    while len(game_board_dict) < 6:
        print(f"<------------------- {round(len(game_board_dict)/6 * 100)}% ------------------->", end="\r")
        category = requests.get('https://jservice.io/api/random')

        if category.status_code == 200:
            category = category.json()[0]
            title = category['category']['title'].title()
            title_id = category['category']['id']
            questions_answers = requests.get(f'https://jservice.io/api/clues?&category={title_id}')

            if questions_answers.status_code == 200:
                questions_answers = questions_answers.json()
                game_board_dict[title] = points
                game_info[title] = {}

                temp_dict = {}

                for question_answer in questions_answers:
                    temp_dict[question_answer['value']] = {'question': question_answer['question'], 'answer': question_answer['answer']}

                if len(temp_dict) < 5:
                    del game_info[title]
                    del game_board_dict[title]
                else:
                    multiply_by_2 = 1

                    for point in points:
                        try:
                            if point in temp_dict:
                                game_info[title][point] = temp_dict[point*multiply_by_2]
                            elif point*2 in temp_dict:  
                                multiply_by_2 = 2
                                game_info[title][point] = temp_dict[point*multiply_by_2]
                            else:
                                raise Exception
                        except:
                            game_info[title][point] = temp_dict[None] 

        time.sleep(1)    

    game_board_dict = pd.DataFrame(game_board_dict)

    return game_board_dict, game_info


def main():
    question_order = {'500': 0, '400': 1, '300': 2, '200': 3, '100': 4 }
    game_board, game_info = start_up()
    player_point = 0
    while True:
        os.system('cls')
        print(f'Score: {player_point}')
        print(game_board.to_string(index=False)) #prints the board too screen
        user_input = input("What question would you like to try in Row Point format? e.g. 2 500: ").strip()
        category, point = tuple(user_input.split(' '))

        title = game_board.columns[int(category)-1]

        if game_board[title].iloc[question_order[point]] != 0:
            game_board[title].iloc[question_order[point]] = 0
            question_info = game_info[title][int(point)]
            question = question_info['question']
            answer = question_info['answer']

            user_guess = input(f'{question}: ')

            if user_guess.lower() == answer.lower():
                print("Correct!")
                player_point += int(point)
            else:
                print(f"Incorrect. The correct answer is {answer}")
        else:
            print("You already answered this section")

        input("Press enter to continue")

main()