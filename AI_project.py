import random
import sys
import pygame
from pygame.locals import *
import numpy
import matplotlib.pyplot as plt

SW = 280 #screen width
SH = 511 #screen height

BASEY = SH *0.8 #base height
IMAGES = {} #dictionary of images
pygame.font.init() #initializing font
WINDOW = pygame.display.set_mode((SW,SH)) #setting window
Font = pygame.font.SysFont("comicsans",20) #setting font
BIRD = 'imgs/bird1.png' #bird image
BG = 'imgs/bg.png' #background image
PIPE = 'imgs/pipe.png' 	#pipe image
Q=numpy.zeros((7,21,2),dtype = float) #Q table size 7*21*2 (x,y,jump or not) initialized to 0 
FPS = 32 #frames per second
def static(): #static screen
	birdxpos = int(SW/5) #bird x position in the screen i.e. 1/5th of the screen width used for centering
	birdypos = int((SH - IMAGES['bird'].get_height())/2) #bird y position in the screen i.e. 1/2 of the screen height - bird height used for centering
	basex = 0 #base x position in the screen i.e. 0 used for scrolling
	while (True): #infinite loop for static screen until space or up key is pressed
		for event in pygame.event.get(): #event handling loop for static screen
			if event.type == QUIT: #if quit button is pressed then quit the game
				pygame.quit() 
				sys.exit()

			elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): #if space or up key is pressed then start the game
				return
			else : #else display the static screen
				WINDOW.blit(IMAGES['background'],(0,0)) #blit background image
				WINDOW.blit(IMAGES['bird'],(birdxpos,birdypos)) #blit bird image at the center of the screen
				WINDOW.blit(IMAGES['base'],(basex,BASEY)) #blit base image at the bottom of the screen
				text1 = Font.render("Flappy Bot",1,(255,255,255)) #render text 
				text2 = Font.render("Yousra",1,(255,255,255))
				WINDOW.blit(text1,(SW/2 ,SH/2)) #blit text at the center of the screen
				WINDOW.blit(text2,(10,50)) #blit text at the top left corner of the screen
				pygame.display.update() #update the display 
				FPSCLOCK.tick(FPS) #tick the clock with FPS

 
def game_start(generation,x,y): #game start function takes generation number and x,y lists for plotting 
	score = 0  #score initialized to 0 
	birdxpos = int(SW/5) #bird x position in the screen i.e. 1/5th of the screen width used for centering
	birdypos = int(SH/2) #bird y position in the screen i.e. 1/2 of the screen height used for centering
	basex1 = 0 #base x position in the screen i.e. 0 used for scrolling 
	basex2 = SW #base x position in the screen i.e. screen width used for scrolling 

	bgx1=0 #background x position in the screen i.e. 0 used for scrolling
	bgx2 = IMAGES['background'].get_width() #background x position in the screen i.e. background width used for scrolling 

	newPipe1 = get_new_pipe() #get new pipe from get_new_pipe function
	newPipe2 = get_new_pipe() #get new pipe 

	up_pipes = [
	{'x':SW +200,'y': newPipe1[0]['y']},
	{'x':SW +500 ,'y': newPipe2[0]['y']}
	] #list of upper pipes 

	bttm_pipes = [
	{'x':SW+200,'y':newPipe1[1]['y']},
	{'x':SW +500 ,'y': newPipe2[1]['y']}
	] #list of bottom pipes

	pipeVelx = -4 #pipe velocity in x direction i.e. -4

	birdyvel = -9 #bird velocity in y direction i.e. -9
	birdymaxvel = 10 #bird maximum velocity in y direction i.e. 10
	birdyvelmin = -8 #bird minimum velocity in y direction i.e. -8
	birdyacc = 1 #bird acceleration in y direction i.e. 1

	playerFlapAccv = -8 #player flap acceleration in y direction i.e. -8
	playerFlapped =False #player flapped boolean variable initialized to false 
	
	while(True): #infinite loop for game start until quit button is pressed
		
		x_prev,y_prev = convert(birdxpos,birdypos,bttm_pipes) #convert bird position and pipe position to x,y coordinates for Q table
		jump = ai_play(x_prev,y_prev) #get jump or not from ai_play function

		for event in pygame.event.get(): #event handling loop for game start screen	
			if event.type == QUIT: 		#if quit button is pressed then quit the game
				plt.scatter(x,y) 		#plot the graph
				plt.xlabel("GENERATION/Number of Trials") 
				plt.ylabel("SCORE")
				plt.title("Flappy Birds : AI Project")
				plt.show()
				pygame.quit() 	
				sys.exit()
				

		if jump: #if jump is true then bird jumps
			if birdypos>0: 		#bird position is greater than 0
				birdyvel = playerFlapAccv  #bird velocity is set to player flap acceleration
				playerFlapped = True 		#player flapped is set to true

		

		
		
		playerMidPos= birdxpos + IMAGES['bird'].get_width()/2 		#player middle position is set to bird x position + bird width/2
		for pipe in up_pipes:  		#loop for upper pipes
			pipeMidPos = pipe ['x'] +IMAGES['pipe'][0].get_width()/2 		#pipe middle position is set to pipe x position + pipe width/2
			if pipeMidPos <= playerMidPos < pipeMidPos +4 : 		#if pipe middle position is less than player middle position and player middle position is less than pipe middle position + 4
				score += 1 			#score is incremented by 1


		if birdyvel < birdymaxvel and not playerFlapped:  #if bird velocity is less than bird maximum velocity and player flapped is false
			birdyvel += birdyacc 		#bird velocity is incremented by bird acceleration


		if playerFlapped: 		#if player flapped is true
			playerFlapped = False 		#player flapped is set to false

		playerHeight = IMAGES['bird'].get_height() 		#player height is set to bird height

		birdypos = birdypos + min (birdyvel, BASEY - birdypos -playerHeight) #bird y position is set to bird y position + minimum of bird velocity, base y position - bird y position - player height

		for upperPipe,lowerPipe in zip(up_pipes,bttm_pipes): 		#loop for upper and bottom pipes
			upperPipe['x'] += pipeVelx 		#upper pipe x position is incremented by pipe velocity in x direction
			lowerPipe['x'] += pipeVelx	    #bottom pipe x position is incremented by pipe velocity in x direction

		if (0<up_pipes[0]['x']<5): 		#if upper pipe x position is greater than 0 and less than 5
			newPipe = get_new_pipe() 		#get new pipe from get_new_pipe function
			up_pipes.append(newPipe[0]) 	#append upper pipe to upper pipe list
			bttm_pipes.append(newPipe[1])   #append bottom pipe to bottom pipe list

		if(up_pipes[0]['x'] < -IMAGES['pipe'][0].get_width() ): #if upper pipe x position is less than negative of pipe width
			up_pipes.pop(0) 	#pop the first element of upper pipe list
			bttm_pipes.pop(0)   #pop the first element of bottom pipe list
		basex1-=4 #base x position is decremented by 4
		basex2-=4 		#base x position is decremented by 4
		if(basex1 <= -IMAGES['base'].get_width()): 		#if base x position is less than negative of base width
			basex1 = basex2 			#base x position is set to base x position 2
			basex2 = basex1 + IMAGES['base'].get_width() 	#base x position 2 is set to base x position + base width

		bgx1-=2 		#background x position is decremented by 2
		bgx2-=2 		#background x position is decremented by 2
		if(bgx1 <= -IMAGES['background'].get_width()): 	#if background x position is less than negative of background width
			bgx1 = bgx2 	#background x position is set to background x position 2
			bgx2 = bgx1 + IMAGES['background'].get_width() 		#background x position 2 is set to background x position + background width
		crashTest = Collision(birdxpos,birdypos,up_pipes,bttm_pipes) 	#crash test is set to collision function
		x_new,y_new = convert(birdxpos,birdypos,bttm_pipes) 	#convert bird position and pipe position to x,y coordinates for Q table
		if crashTest: 		#if crash test is true
			reward = -1000 		#reward is set to -1000
			Q_update(x_prev,y_prev,jump,reward,x_new,y_new) 		#update Q table
			return score 		#return score

		reward = 15 		#reward is set to 15

		Q_update(x_prev,y_prev,jump,reward,x_new,y_new) 		#update Q table

		WINDOW.blit(IMAGES['background'],(bgx1,0)) 		#blit background image
		WINDOW.blit(IMAGES['background'],(bgx2,0)) 		#blit background image
		for upperPipe,lowerPipe in zip(up_pipes,bttm_pipes): 		#loop for upper and bottom pipes 
			WINDOW.blit(IMAGES['pipe'][0],(upperPipe['x'],upperPipe['y'])) 		#blit upper pipe image for pipe 0
			WINDOW.blit(IMAGES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))  	#blit bottom pipe image for pipe 1
		WINDOW.blit(IMAGES['base'],(basex1,BASEY)) 		#blit base image for base 1
		WINDOW.blit(IMAGES['base'],(basex2,BASEY)) 		#blit base image for base 2 
		text1 = Font.render("Score: "+ str(score),1,(255,255,255)) 		#render text of score
		text2 = Font.render("Generation: "+ str(generation),1,(255,255,255)) 	#render text of generation
		WINDOW.blit(text1,(SW - 10 -text1.get_width(),10)) 		#blit text of score in the top right corner of the screen
		WINDOW.blit(text2,(0,0)) 		#blit text of generation in the top left corner of the screen
		WINDOW.blit(IMAGES['bird'],(birdxpos,birdypos)) 		#blit bird image at the center of the screen

		pygame.display.update() 		#update the display for every frame
		FPSCLOCK.tick() 		#tick the clock with FPS

def Collision(birdxpos,birdypos,up_pipes,bttm_pipes): #collision function takes bird x position, bird y position, upper pipe list and bottom pipe list
	if (birdypos >= BASEY - IMAGES['bird'].get_height() or birdypos < 0): #if bird y position is greater than base y position - bird height or bird y position is less than 0
		return True #return true
	for pipe in up_pipes: 		#loop for upper pipes to check collision
		pipeHeight = IMAGES['pipe'][0].get_height() 		#pipe height is set to pipe height
		if(birdypos < pipeHeight + pipe['y'] and abs(birdxpos - pipe['x']) < IMAGES['pipe'][0].get_width()): #if bird y position is less than pipe height + pipe y position and absolute value of bird x position - pipe x position is less than pipe width
			return True 

	for pipe in bttm_pipes: 		#loop for bottom pipes to check collision
		if (birdypos + IMAGES['bird'].get_height() > pipe['y'] and abs(birdxpos - pipe['x']) < IMAGES['pipe'][0].get_width()): 	#if bird y position + bird height is greater than pipe y position and absolute value of bird x position - pipe x position is less than pipe width
			return True
	return False


def get_new_pipe(): #get new pipe function which returns new pipe to replace the old pipe 

	pipeHeight = IMAGES['pipe'][1].get_height() #pipe height is set to pipe height from image dictionary
	gap = int(SH/4) #gap is set to 1/4th of the screen height which is 127 
	y2 = int(gap + random.randrange(0,int(SH - IMAGES['base'].get_height() - 1.2*gap))) #y2 is set to gap + random number between 0 and screen height - base height - 1.2*gap
	pipex = int(SW+300 ) 		#pipe x position is set to screen width + 300
	y1 = int(pipeHeight -y2 +gap) 	#y1 is set to pipe height - y2 + gap

	pipe = [
	{'x':pipex,'y':-y1},
	{'x':pipex,'y':y2}
	] 		#pipe list is set to pipe x position and y1 and y2
	return pipe

def ai_play(x,y): #ai play function takes x,y coordinates from Q table and returns jump or not
	max=0 #max is set to 0
	jump = False 		#jump is set to false
	
	
	if(Q[x][y][1]>Q[x][y][0]): 		#if Q table value of x,y,1 is greater than Q table value of x,y,0
		max = Q[x][y][1] 		#max is set to Q table value of x,y,1
		jump =True 		#jump is set to true

	return jump 		#return jump

def convert(birdxpos,birdypos,bttm_pipes): #convert function takes bird x position, bird y position and bottom pipe list and returns x,y coordinates for Q table
	x = min(280, bttm_pipes[0]['x']) 		#x is set to minimum of 280 and bottom pipe x position
	y = bttm_pipes[0]['y']-birdypos 		#y is set to bottom pipe y position - bird y position
	if(y<0): 		#if y is less than 0
		y=abs(y)+408 		#y is set to absolute value of y + 408 to get positive value
	return int(x/40-1),int(y/40) 			#return x/40-1 and y/40 to get x,y coordinates for Q table


def Q_update(x_prev,y_prev,jump,reward,x_new,y_new): #Q update function takes x,y coordinates from Q table, jump or not, reward and new x,y coordinates from Q table


	if jump: 		#if jump is true then Q table value of x,y,1 is updated 
		Q[x_prev][y_prev][1] = 0.4 * Q[x_prev][y_prev][1] + (0.6)*(reward+max(Q[x_new][y_new][0],Q[x_new][y_new][1])) 	
	else : 		#else Q table value of x,y,0 is updated
		Q[x_prev][y_prev][0] = 0.4 * Q[x_prev][y_prev][0] + (0.6)*(reward+max(Q[x_new][y_new][0],Q[x_new][y_new][1]))



if __name__=="__main__": #main function

	pygame.init() #initializing pygame
	FPSCLOCK = pygame.time.Clock() 	#setting clock for FPS
	pygame.display.set_caption("AI PROJECT") 	#setting caption for the game

	IMAGES['base'] = pygame.image.load('imgs/base.png').convert_alpha() #loading base image
	IMAGES['pipe'] = ( pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180) , pygame.image.load(PIPE).convert_alpha()) 	#loading pipe image
	IMAGES['background']= pygame.image.load(BG).convert() 		#loading background image
	IMAGES['bird'] = pygame.image.load(BIRD).convert_alpha() 	#loading bird image
	generation = 1 #generation initialized to 1
	static() #calling static function which displays static screen
	x=[] #x list for plotting
	y=[] #y list for plotting
	while(True): #infinite loop for game start
		score = game_start(generation,x,y) #score is set to game start function
		if (score==-1): #if score is -1 then break the loop
			break
		x.append(generation) #append generation to x list for plotting
		y.append(score) #append score to y list for plotting
		generation+=1 #increment generation by 1
	
		
	print(generation) #print generation


