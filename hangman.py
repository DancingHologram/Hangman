import wordlist
import pygame
import sys
import constants
from button import Button

class Hangman:
    def __init__(self, word, word_length, remaining_letters, displayed_word, num_wrong, num_guesses, guessed_letters):
        self.word = word
        self.word_length = word_length
        self.remaining_letters = remaining_letters
        self.displayed_word = displayed_word
        self.num_wrong = num_wrong
        self.num_guesses = num_guesses
        self.guessed_letters = guessed_letters

    def reset_game(self):
        self.word = get_word()
        self.word_length = len(self.word)
        self.remaining_letters = self.word_length
        self.displayed_word = "_" * self.word_length
        self.num_wrong = 0               
        self.num_guesses = 0
        self.guessed_letters = ""

    def get_letter(self, letter):
        if letter in self.guessed_letters:
            return False
        else:
            self.guessed_letters += letter
            return True
            
    def draw_screen(self, surface):
        surface.fill(constants.WHITE)  # Clear the screen with white background
        font = pygame.font.Font(None, constants.WORD_FONT_SIZE)
        text = font.render(f"Word: {add_spaces(self.displayed_word)}  Guesses: {self.num_guesses}  Wrong: {self.num_wrong}  Tried: {add_spaces(self.guessed_letters)}", True, constants.BLACK)
        surface.blit(text, (20, 20))
        pygame.display.flip()

    def init_menu_state(self):
        self.menu_button = Button(400, 300, 200, 50, "Play Game")
        self.add_word_button = Button(400, 360, 200, 50, "Add Word")
        self.quit_button = Button(400, 400, 200, 50, "Quit")

    def handle_menu_events(self, event, menu_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.menu_button.is_clicked(mouse_x, mouse_y):
                self.reset_game()
                return "play"
            elif self.add_word_button.is_clicked(mouse_x, mouse_y):
                return "add_word"
            elif self.quit_button.is_clicked(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()
        return menu_state
    
    def draw_menu(self, surface, menu_state):
        surface.fill(constants.WHITE)  # Clear the screen with white background
        font = pygame.font.Font(None, constants.TITLE_FONT_SIZE)
        title_text = font.render("Welcome to Hangman!", True, constants.BLACK)
        surface.blit(title_text, (constants.GAME_WIDTH // 2 - title_text.get_width() // 2, 100))
        self.menu_button.draw(surface)
        self.add_word_button.draw(surface)
        self.quit_button.draw(surface)
        pygame.display.flip()

# Get a random word from the word list
def get_word():
    word = wordlist.get_random_word()
    return word.upper()

# Add spaces between letters
def add_spaces(word):
    word_with_spaces = " ".join(word)
    return word_with_spaces

# Draw the display
def draw_screen(num_wrong, num_guesses, guessed_letters, displayed_word):
    pass

# Get next letter from user
def get_letter(guessed_letters):
    pass


# The input/process/draw technique is common in game programming
def play_game():
    word = get_word()
    
    word_length = len(word)
    remaining_letters = word_length
    displayed_word = "_" * word_length

    num_wrong = 0               
    num_guesses = 0
    guessed_letters = ""

    draw_screen(num_wrong, num_guesses, guessed_letters, displayed_word)

    while num_wrong < 10 and remaining_letters > 0:
        guess = get_letter(guessed_letters)
        guessed_letters += guess
        
        pos = word.find(guess, 0)
        if pos != -1:
            displayed_word = ""
            remaining_letters = word_length
            for char in word:
                if char in guessed_letters:
                    displayed_word += char
                    remaining_letters -= 1
                else:
                    displayed_word += "_"              
        else:
            num_wrong += 1

        num_guesses += 1

        draw_screen(num_wrong, num_guesses, guessed_letters, displayed_word)

def display_menu():
    pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    pygame.display.set_caption("Hangman")
    
    hangman = Hangman("", 0, 0, "", 0, 0, "")
    hangman.draw_menu(screen)

if __name__ == "__main__":
    main()