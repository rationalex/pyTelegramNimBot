import enum
import functools
import config


class GameException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.message = message


class Turn(enum.Enum):
    PLAYER = 1
    AI = 2


class GameState(enum.Enum):
    NOT_STARTED = 0
    IN_PROCESS = 1
    FINISHED = 2


class Game:
    """
    This class contains all information about game with user
    And handles all interactions between user and game

    Game data:
        -- player_id               -- Telegram chat ID of user

        -- state                   -- one of GameState.NotStarted,
                                           GameState.InProcess,
                                           GameState.Finished

        -- piles_size -- List[Int] -- list of current sizes of piles

        -- whose_turn              -- Turn.Player || Turn.AI
    """

    DEFAULT_PILES_SIZES = [10, 11, 179]

    def __init__(self,
                 player_id,
                 piles_sizes=DEFAULT_PILES_SIZES,
                 whose_turn=Turn.PLAYER):
        self.player_id = player_id
        self.piles_sizes = piles_sizes
        self.whose_turn = whose_turn
        self.state = GameState.IN_PROCESS

    def finish(self):
        self.state = GameState.FINISHED

    def reduce_pile(self,
                    num_pile,
                    cnt_stones):
        """
            num_pile: one of [1, ..., len(self.current_piles)]
            cnt stones: number of stones to be removed
        """
        if len(self.piles_sizes) < num_pile:
            raise GameException("Invalid pile number: {}".format(num_pile))
        num_pile -= 1

        if self.piles_sizes[num_pile] < cnt_stones:
            raise GameException("\
            Invalid number of stones: {}".format(cnt_stones))

        self.piles_sizes[num_pile] -= cnt_stones
        if self.piles_sizes[num_pile] == 0:
            self.piles_sizes.pop(num_pile)

    def optimal_turn(self):
        """
            if there is winning turn for current position
            returns number of pile and amount of stones to be taken
            otherwise, returns (1, 1)
        """

        # n1 ^ n2 ^ n3 ^ ... ^ nk
        # where ni is number of piles in pile number i
        # and ^ is binary XOR
        s = functools.reduce(lambda x, y: x ^ y, self.piles_sizes)
        if s == 0:
            return 1, 1
        else:
            max_bit = len(bin(s)[2:]) - 1
            for i, pile_size in enumerate(self.piles_sizes):
                if Game.has_bit(pile_size, max_bit):
                    pile_num = i + 1
                    should_be_after = s ^ pile_size
                    to_remove = pile_size - should_be_after
                    return pile_num, to_remove

    @staticmethod
    def has_bit(number, bit):
        binary = bin(number)[2:][::-1]
        if len(binary) <= bit:
            return False

        return (bin(number)[2:])[::-1][bit] == '1'

    def accept_turn_from_player(self, pile_num, num_deleted):
        """

        :param pile_num:
        :param num_deleted:
        :return: game state after turn completion
        """
        if self.whose_turn != Turn.PLAYER:
            raise GameException(config.NOT_PLAYERS_TURN_ERR)

        self.reduce_pile(pile_num, num_deleted)
        self.remove_empty_piles()

        self.whose_turn = Turn.AI

        return self.piles_sizes

    def perform_ai_turn(self):
        """

        :return: piles after AI turn
        """
        if self.whose_turn != Turn.AI:
            raise GameException("\
            AI can't perform turn, it's player's turn now")

        optimal_pile, optimal_stones_num = self.optimal_turn()
        self.reduce_pile(optimal_pile, optimal_stones_num)
        self.remove_empty_piles()

        self.whose_turn = Turn.PLAYER
        return self.piles_sizes

    def is_finished(self):
        return self.state == GameState.FINISHED

    def remove_empty_piles(self):
        self.piles_sizes = list(filter(lambda size: size != 0,
                                       self.piles_sizes))
