import json
from pathlib import Path
import random


class User:

    def __init__(self):
        self.username = self.login()
        self.score = 0

    @staticmethod
    def get_new_username(all_usernames, username):
        while username in all_usernames:
            print(f'Username {username} already in use. Please enter a new username')
            username = input('Enter username: ')
        return username

    @staticmethod
    def authenticated(user_data):
        # Give the user three attempts to enter a valid password
        # If this is unsuccessful then they need to make a new account
        logged_in = False
        password = input('Enter password: ')
        for _ in range(3):
            if user_data['password'] == password:
                print('Login successful :)')
                logged_in = True
                break
            password = input('Incorrect password. Please enter a valid password: ')
        return logged_in

    def login(self):
        """
        Ensure that the user is logged in correctly (creating a new account if required)
        :return: The username for the user
        :rtype: str
        """
        has_account = input(f'Have you got an account? (y/n)').lower() == 'y'
        username = input('Enter username: ')
        all_user_data = self.get_all_user_data()

        if has_account:
            if username in all_user_data:
                if self.authenticated(all_user_data[username]):
                    return username
                print('Too many failed login attempts. Creating a new account')
            else:
                # User said they had an account but it can not be found, so create a new one
                print(f'User account "{username}" not found, creating a new account with username {username}')

        username = self.get_new_username(all_user_data.keys(), username)
        password = input('Enter a password: ')
        all_user_data.update({username: {'password': password, 'highscore': '0'}})
        self.write_all_user_data(all_user_data)
        return username

    def play(self):
        total = Dice(self.username).play()
        self.score += total
        if self.score < 0:
            self.score = 0
        print(f'{self.username} your score is {self.score}')

    def check_highscore(self):
        all_user_data = self.get_all_user_data()
        existing_highscore = int(all_user_data[self.username].get('highscore', 0))
        if self.score > existing_highscore:
            print(f'\nCongratulations!!! Previous highscore: {existing_highscore}!\nNew highscore {self.score}')
            all_user_data[self.username]['highscore'] = str(self.score)
            self.write_all_user_data(all_user_data)

    @staticmethod
    def get_all_user_data():
        user_data_path = Path('users.txt')
        if not user_data_path.exists():
            return {}
        with open('users.txt', 'r') as user_file:
            contents = user_file.read()
            if not contents:
                contents = '{}'
            return json.loads(contents)

    @staticmethod
    def write_all_user_data(all_user_data):
        with open('users.txt', 'w') as user_file:
            user_file.write(json.dumps(all_user_data, indent=4))


class Dice:

    def __init__(self, username):
        self.username = username

    @staticmethod
    def roll(die_name):
        die_total = random.randint(1, 6)
        print(f'{die_name} is:', die_total)
        return die_total

    def play(self):
        input(f'{self.username}: Press enter to play.\n')
        dice1 = self.roll('Dice one')
        dice2 = self.roll('Dice two')

        total = dice1 + dice2
        print(f'Total score {total}')

        return total + self.adjusted(total)

    def adjusted(self, total):
        adjustment = 0
        mod = total % 2
        if mod > 0:
            print(f'Sorry! Roll total was odd. {self.username} loses 5 points...')
            adjustment = -5
        elif mod == 0:
            print(f'Yippee! Roll total was even. {self.username} gains 10 points...')
            adjustment = 10
        return adjustment


def main():
    print('\nWelcome!\n')
    print('This is a game where each player takes turns to roll two dice. Scoring rules...')
    print('If the sum of the two dice is even, you get the sum of the dice plus 10 points.')
    print('However, if the sum is odd, you get the sum of the dice minus 5 points!')

    print('\nUser1 login.')
    user1 = User()
    print('\nUser2 login.')
    user2 = User()

    # Play!
    for n in range(1, 6):
        print(f'\n\nRound {n}!\n')
        user1.play()
        user2.play()

    user1.check_highscore()
    user2.check_highscore()


if __name__ == '__main__':
    main()
