
from pieces import *
from typing import List, Tuple


def position_to_rect(position: List[int]) -> Tuple[int]:
    return (position % 8) * 100, (position // 8) * 100, 100, 100


def mouse_cord() -> int:
    return 8 * (pygame.mouse.get_pos()[1] // 100) + pygame.mouse.get_pos()[0] // 100


class Game:
    def __init__(self):
        pygame.init()
        self.size = (800, 800)
        self.screen = pygame.display.set_mode(self.size)
        self.running = True
        self.clock = pygame.time.Clock()
        self.draw_chessboard()
        self.bluetomove = True
        self.allpieces = AllPieces()
        self.ismoving = False
        self.piecemoving = None
        self.morecaptures = False
        self.allpieces.find_all_possible_moves(self.bluetomove)

    def draw_chessboard(self) -> None:
        for i in range(64):
            if (i + (i // 8) % 2) % 2 == 0:
                pygame.draw.rect(self.screen, (232, 218, 161), pygame.Rect((i % 8) * 100, (i // 8) * 100, 100, 100))
            else:
                pygame.draw.rect(self.screen, (148, 105, 30), pygame.Rect((i % 8) * 100, (i // 8) * 100, 100, 100))

    def draw_possible_moves(self, pieceindex) -> None:
        if not self.allpieces.captures:
            for position in self.allpieces.possiblemoves[pieceindex]:
                self.screen.blit(pygame.image.load('assets/move.png'), position_to_rect(position))
        for capture in self.allpieces.captures:
            if capture[0] == pieceindex:
                self.screen.blit(pygame.image.load('assets/move.png'), position_to_rect(capture[1]))

    def move(self):
        mouseposition = mouse_cord()
        for i in range(len(self.allpieces.allpieces[int(self.bluetomove)])):
            if mouseposition == self.allpieces.allpieces[int(self.bluetomove)][i].position:
                self.ismoving = True
                self.piecemoving = i
        if self.ismoving:
            if self.allpieces.captures:
                for values in self.allpieces.captures:
                    if mouseposition == values[1]:
                        self.allpieces.allpieces[int(self.bluetomove)][self.piecemoving].position = mouseposition
                        self.allpieces.remove_piece(not self.bluetomove, values[2])
                        self.allpieces.clear_caputres()
                        self.allpieces.find_possible_moves(self.allpieces.allpieces[int(self.bluetomove)][self.piecemoving], self.bluetomove)
                        if not self.allpieces.captures:
                            self.end_move()
                        else:
                            self.morecaptures = True
            elif mouseposition in self.allpieces.possiblemoves[self.piecemoving]:
                self.allpieces.allpieces[int(self.bluetomove)][self.piecemoving].position = mouseposition

                self.end_move()

    def end_move(self):
        if self.allpieces.allpieces[int(self.bluetomove)][self.piecemoving].position // 8 == 7 - 7 * int(
                self.bluetomove):
            self.allpieces.allpieces[int(self.bluetomove)][self.piecemoving].queen()
        self.morecaptures = False
        self.ismoving = False
        self.piecemoving = None
        self.bluetomove = not self.bluetomove
        self.allpieces.find_all_possible_moves(self.bluetomove)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.move()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.morecaptures:
                self.end_move()

    def on_loop(self):
        pass

    def on_render(self):
        self.draw_chessboard()

        if self.ismoving:
            self.draw_possible_moves(self.piecemoving)
        for piece in self.allpieces.allpieces[0]:
            self.screen.blit(piece.image, pygame.Rect(position_to_rect(piece.position)))
        for piece in self.allpieces.allpieces[1]:
            self.screen.blit(piece.image, pygame.Rect(position_to_rect(piece.position)))
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self.running:
            if len(self.allpieces.allpieces[0]) == 0:
                print("Blue wins")
                self.running = False
            if len(self.allpieces.allpieces[1]) == 0:
                print("Red wins")
                self.running = False
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
            self.clock.tick(60)
        self.on_cleanup()
