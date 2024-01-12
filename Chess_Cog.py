import discord
from discord.ext import commands
import chess
import chess.svg
import torch
from NeuralNets import NeuralNetwork_corrected
from play_update import move, eval
from fentoimage.board import BoardImage
import imageio
import helpers
from stockfish import Stockfish

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.board = chess.Board()
        self.color = chess.WHITE
        self.opponent = None
        self.game = False
        self.engine = NeuralNetwork_corrected(769, [770,512,256,128,64,32,16,1])
        self.engine.load_state_dict(torch.load("SendHelpPls/Schopp_Bot/ShessGPT_2_57.pth", map_location = torch.device('cpu')))

    @staticmethod
    def store_img(fen, bot_move):
        renderer = BoardImage(fen)
        print(bot_move)
        if bot_move is not None:
            image = renderer.render(highlighted_squares=(bot_move.from_square, bot_move.to_square))
            imageio.imwrite('SendHelpPls/Schopp_Bot/board.png', image)
        else:
            image = renderer.render()
            imageio.imwrite('SendHelpPls/Schopp_Bot/board.png', image)

    
    def reset(self):
        self.board = chess.Board()
        self.color = chess.WHITE
        self.opponent = None
        self.game = False

    
    async def check_result(self, ctx):
        if self.board.is_game_over():
            if self.board.is_checkmate():
                reason = 'Checkmate'
            elif self.board.is_stalemate():
                reason = 'Stalemante'
            elif self.board.is_insufficient_material():
                reason = 'Insufficient Material'
            elif self.board.is_fivefold_repetition():
                reason = 'Fivefold Repetition'
            result = self.board.result()
            await ctx.channel.send(f'The game is over. Result: {result}, Reason: {reason}')
            self.store_img(self.board.fen(), None)
            await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
            self.reset()
            return True
        return False

    @commands.command(name='chess')
    async def _chess(self, ctx: commands.Context, *, color: str):
        '''start es schach spiel. gib a welli farb DU spiele willsch'''
        if not self.game:
            self.opponent = ctx.author.display_name
            if color.lower() == 'white':
                await ctx.send('Du spielsch wiss!')
                self.color = chess.BLACK
                self.game = True
                self.store_img(self.board.fen(), None)
                await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
            elif color.lower() == 'black':
                await ctx.send('Du spielsch schwarz!')
                self.color = chess.WHITE
                self.game = True
                best_move, eval = move(self.engine, self.board, self.color)
                store = best_move
                self.board.push(best_move)
                self.store_img(self.board.fen(), store)
                await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
            else:
                raise commands.CommandError('Du muesch no e farb schriibe entwecker "white" oder "black" z.B !chess white, denn spielsch als white')
        else:
            await ctx.channel.send("Es lauft scho es spiel")
    
    @commands.command(name='move')
    async def _move(self, ctx: commands.Context, *, player_move: str):
        '''Mach Move im Format vo wellem zu wellem Feld. z.B e2e4'''
        if self.opponent != ctx.author.display_name or self.game == False:
            await ctx.channel.send("Du bisch nöd de gegner, hör uf probiere griefe, oder es lauft gar keis game")
            return
        spielzug = chess.Move.from_uci(player_move)
        try:
            if spielzug in self.board.legal_moves:
                self.board.push(spielzug)
                if await self.check_result(ctx) == False:
                    bot_move, eval = move(self.engine, self.board, self.color)
                    self.board.push(bot_move)
                    if await self.check_result(ctx) == False:
                        self.store_img(self.board.fen(), bot_move)
                        await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
            else:
                await ctx.channel.send(f'Das isch kein legal move gsi, das sind die mögliche Züg: {list(self.board.legal_moves)}')
        except:
            await ctx.channel.send(f'Das isch kein legal move gsi, das sind die mögliche Züg: {list(self.board.legal_moves)}')
        
    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context):
        '''stockfish und ShessGPT eval'''
        stockfish = Stockfish(path="/home/arbeite/stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads":4})
        stockfish_eval = helpers.get_stockfish_eval(stockfish, self.board)
        shess_gpt_eval = eval(self.board, self.engine)

        await ctx.channel.send(f'Stockfish: {stockfish_eval}, ShessGPT: {shess_gpt_eval.item()}')
    
    @commands.command('finish')
    async def _finish(self, ctx: commands.Context):
        '''es beendet es spiel, chan jede user mache'''
        self.reset()
        await ctx.channel.send(f'{ctx.author.display_name} has just terminated the game!')
    
    @commands.command('undo')
    async def _undo(self, ctx: commands.Context):
        '''undo din vorherige zug'''
        if ctx.author.display_name == self.opponent and self.game == True:
            self.board.pop()
            self.board.pop()
            self.store_img(self.board.fen(), None)
            await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
        else:
            ctx.channel.send(f'{ctx.author.display_name} du bisch nöd dra amk, oder es lauft gar keis game')

    @commands.command('make_move')
    async def _different_move(self, ctx: commands.Context, *, player_move: str):
        '''Du chasch en Move mache für de Bot'''
        if ctx.author.display_name == self.opponent and self.game == True:
            self.board.pop()
            spielzug = chess.Move.from_uci(player_move)
            try:
                if spielzug in self.board.legal_moves:
                    self.board.push(spielzug)
                    if await self.check_result(ctx) == False:
                        self.store_img(self.board.fen(), spielzug)
                        await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
                else:
                    await ctx.channel.send(f'Das isch kein legal move gsi, das sind die mögliche Züg: {list(self.board.legal_moves)}')
            except:
                await ctx.channel.send(f'Das isch kein legal move gsi, das sind die mögliche Züg: {list(self.board.legal_moves)}')

    @commands.command('chess_fen')
    async def _chess_fen(self, ctx: commands.Context, *, fen_color: str):
        '''start es spiel vonere FEN position. Format(Komma, Leertaste) vom befehl wichtig. z.B .chess_fen r1bqkbnr/2pp1ppp/p1n5/1p2p3/B3P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 5, black'''
        words = fen_color.split(', ',1)
        fen = words[0]
        color = words[1]
        self.board = chess.Board(fen)
        self.opponent = ctx.author.display_name
        if self.board.turn and ctx.author.display_name == self.opponent:
            if not self.game:
                if color.lower() == 'white':
                    await ctx.send('Du spielsch wiss!')
                    self.color = chess.BLACK
                    self.game = True
                    self.store_img(self.board.fen(), None)
                    await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
                elif color.lower() == 'black':
                    await ctx.send('Du spielsch schwarz!')
                    self.color = chess.WHITE
                    self.game = True
                    best_move, eval = move(self.engine, self.board, self.color)
                    store = best_move
                    self.board.push(best_move)
                    self.store_img(self.board.fen(), store)
                    await ctx.channel.send(file=discord.File('SendHelpPls/Schopp_Bot/board.png'))
                else:
                    raise commands.CommandError('Du muesch no e farb schriibe entwecker "white" oder "black" z.B !chess white, denn spielsch als white')
            else:
                await ctx.channel.send("Es lauft scho es spiel")
        else:
            await ctx.channel.send("FEN position sött so gwählt sie, dass Wiss am Zug isch. Denk dra, du hesch no undo befehl und make_move, oder du bisch nöd am spiele amk")
    @commands.command('suggestion')
    async def _suggestion(self, ctx: commands.Context):
        '''Stockfish and ShessGPT will give move suggestion of the current board'''
        if self.game == True:
            best_move, eval = move(self.engine, self.board, self.color)
            stockfish = Stockfish(path="/home/arbeite/stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads":4})
            stockfish.set_fen_position(self.board.fen())
            best_stockfish = stockfish.get_best_move()
            await ctx.channel.send(f'Stockfish: {best_stockfish}, ShessGPT: {best_move}')
        else:
            await ctx.channel.send("Es lauft grad gar keis game")

    @commands.command('fen')
    async def _fen(self, ctx: commands.Context):
        '''Get FEN from the current position'''
        if self.game == True:
            await ctx.channel.send(f"The FEN of the current position is: {self.board.fen()}")
        else:
            await ctx.channel.send("Es lauft grad gar keis game")