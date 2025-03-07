import pygame


class Piece:
    def __init__(self, position: int, isblue: bool, isqueen=False):
        self.position = position
        self.isblue = isblue
        self.isqueen = isqueen
        self.image = pygame.image.load('assets/blue_checker.png') if isblue else pygame.image.load('assets/red_checker.png')

    def queen(self):
        self.isqueen = True
        self.image = pygame.image.load('assets/blue_queen.png') if self.isblue else pygame.image.load('assets/red_queen.png')


class AllPieces:
    def __init__(self):
        self.allpieces = [[Piece(i * 2 + 1 - (i // 4 % 2), False) for i in range(12)],
                          [Piece(i * 2 + 40 + (i // 4 % 2), True) for i in range(12)]]
        self.captures = []
        self.possiblemoves = []

    def get_all_positions(self) -> tuple[list[int], list[int]]:
        return [piece.position for piece in self.allpieces[0]], [piece.position for piece in self.allpieces[1]]

    def remove_piece(self, bluetomove: bool, index: int) -> None:
        self.allpieces[int(bluetomove)].pop(index)

    def find_all_possible_moves(self, bluetomove: bool) -> None:
        self.captures = []
        self.possiblemoves = []
        for piece in self.allpieces[int(bluetomove)]:
            self.find_possible_moves(piece, bluetomove)

    def clear_caputres(self) -> None:
        self.captures = []

    def find_possible_moves(self, piece: Piece, bluetomove: bool):
        allpositions = self.get_all_positions()
        if piece.isqueen:
            piececaptured = 0
            possiblemoves = []
            for i in range(4):
                isaftercapture = False
                move = piece.position
                previousrank = move // 8
                while 0 <= move <= 63:
                    move = move + 7 + 2 * (i % 2) if i < 2 else move - 7 - 2 * (i % 2)
                    if abs(move // 8 - previousrank) != 1:
                        break
                    if move in allpositions[int(piece.isblue)] and not isaftercapture:
                        break
                    elif move in allpositions[int(not piece.isblue)]:
                        if isaftercapture:
                            break
                        else:
                            piececaptured = move
                            isaftercapture = True
                    elif isaftercapture and move not in allpositions[0] and move not in allpositions[1]:
                        self.captures.append([self.allpieces[int(bluetomove)].index(piece), move,
                                              allpositions[not piece.isblue].index(piececaptured)])
                    else:
                        possiblemoves.append(move)
                    previousrank = move // 8
        else:
            possiblemoves = [piece.position - 7 if bluetomove else piece.position + 7,
                             piece.position - 9 if bluetomove else piece.position + 9]
            if bluetomove:
                if possiblemoves[0] // 8 != piece.position // 8 - 1:
                    possiblemoves.pop(0)
                if possiblemoves[-1] // 8 != piece.position // 8 - 1:
                    possiblemoves.pop(-1)
            else:
                if possiblemoves[0] // 8 != piece.position // 8 + 1:
                    possiblemoves.pop(0)
                if possiblemoves[-1] // 8 != piece.position // 8 + 1:
                    possiblemoves.pop(-1)
            for allypiece in self.allpieces[int(bluetomove)]:
                if allypiece.position in possiblemoves:
                    possiblemoves.remove(allypiece.position)
            for enemypiece in self.allpieces[int(not bluetomove)]:
                if enemypiece.position in possiblemoves:
                    possiblemoves.remove(enemypiece.position)
                    positionaftercapture = (enemypiece.position - piece.position) * 2 + piece.position
                    if positionaftercapture not in allpositions[0] and positionaftercapture not in allpositions[
                        1] and \
                            positionaftercapture // 8 == piece.position // 8 + 2 - 4 * int(bluetomove) and \
                            0 < positionaftercapture // 8 < 8:
                        # add to capturs list [index of piece, positionaftercapture, index of enemypiece]
                        self.captures.append([self.allpieces[int(bluetomove)].index(piece), positionaftercapture,
                                              self.allpieces[int(not bluetomove)].index(enemypiece)])

        self.possiblemoves.append(possiblemoves)
