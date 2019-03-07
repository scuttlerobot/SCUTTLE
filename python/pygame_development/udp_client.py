import pygame
import socket

serverIP = "192.168.8.1"	# Beagle Bone AP Default Gateway IP
#clientIP = "192.168.8.137"	# Beagle Bone AP Default Gateway IP

#clientPORT = 6970
serverPORT = 6969		# Beagle Bone DSTR Server Port

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

pygame.init()

display_size = [400,500]

screen = pygame.display.set_mode((display_size[0],display_size[1]))
pygame.display.set_caption('SCUTTLE Controller')

font = pygame.font.SysFont("comicsansms", 28)

textsurface = font.render('SCUTTLE Controller', False, (0, 0, 0))

white = (255,255,255)

arrow_size = 100

clock = pygame.time.Clock()

done = False

left_arrow = pygame.image.load('./left_arrow.png')
left_arrow_pressed = pygame.image.load('./left_arrow_pressed.png')

right_arrow = pygame.image.load('./right_arrow.png')
right_arrow_pressed = pygame.image.load('./right_arrow_pressed.png')

up_arrow = pygame.image.load('./up_arrow.png')
up_arrow_pressed = pygame.image.load('./up_arrow_pressed.png')

down_arrow = pygame.image.load('./down_arrow.png')
down_arrow_pressed = pygame.image.load('./down_arrow_pressed.png')


left_arrow = pygame.transform.scale(left_arrow, (arrow_size, arrow_size))
left_arrow_pressed = pygame.transform.scale(left_arrow_pressed, (arrow_size, arrow_size))

right_arrow = pygame.transform.scale(right_arrow, (arrow_size, arrow_size))
right_arrow_pressed = pygame.transform.scale(right_arrow_pressed, (arrow_size, arrow_size))

up_arrow = pygame.transform.scale(up_arrow, (arrow_size, arrow_size))
up_arrow_pressed = pygame.transform.scale(up_arrow_pressed, (arrow_size, arrow_size))

down_arrow = pygame.transform.scale(down_arrow, (arrow_size, arrow_size))
down_arrow_pressed = pygame.transform.scale(down_arrow_pressed, (arrow_size, arrow_size))



screen.fill(white)

screen.blit(textsurface,(30,30))


screen.blit(left_arrow,(50,200))
screen.blit(right_arrow,(250,200))

screen.blit(up_arrow,(150,110))
screen.blit(down_arrow,(150,300))



while done==False:

	data = b""
	
	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:
	
			if event.key == pygame.K_LEFT:
				data = b"0"					
				screen.blit(left_arrow_pressed,(50,200))

			elif event.key == pygame.K_RIGHT:
				data = b"1"
				screen.blit(right_arrow_pressed,(250,200))				

			elif event.key == pygame.K_UP:
				data = b"2"
				screen.blit(up_arrow_pressed,(150,110))				
	
			elif event.key == pygame.K_DOWN:
				data = b"3"
				screen.blit(down_arrow_pressed,(150,300))
				
			elif event.key == pygame.K_RSHIFT:
				data = b"4"
				
			elif event.key == pygame.K_SPACE:
				data = b"5"
				
			elif event.key == pygame.K_ESCAPE:
				done = True
			
		if event.type == pygame.KEYUP:

			if event.key == pygame.K_LEFT:
				data = b"0"					
				screen.blit(left_arrow,(50,200))

			elif event.key == pygame.K_RIGHT:
				data = b"1"
				screen.blit(right_arrow,(250,200))				

			elif event.key == pygame.K_UP:
				data = b"2"
				screen.blit(up_arrow,(150,110))				
	
			elif event.key == pygame.K_DOWN:
				data = b"3"
				screen.blit(down_arrow,(150,300))
		
		if event.type == pygame.MOUSEBUTTONDOWN:
		    # Set the x, y postions of the mouse click
			x, y = event.pos

			if left_arrow.get_rect().collidepoint(x, y):
				screen.blit(left_arrow_pressed,(50,200))

			if right_arrow.get_rect().collidepoint(x, y):
				screen.blit(right_arrow_pressed,(250,200))

			if up_arrow.get_rect().collidepoint(x, y):
				screen.blit(up_arrow_pressed,(150,110))

			if down_arrow.get_rect().collidepoint(x, y):
				screen.blit(down_arrow_pressed,(150,300))

			print("down ", x,y)

		if event.type == pygame.MOUSEBUTTONUP:
		    # Set the x, y postions of the mouse click
			x, y = event.pos

			screen.blit(left_arrow,(50,200))
			screen.blit(right_arrow,(250,200))
			screen.blit(up_arrow,(150,110))
			screen.blit(down_arrow,(150,300))

			print("up ",x,y)


	pygame.display.update()
	clock.tick(60)
	
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.sendto(data, (serverIP, serverPORT))

#	print('sent')

#	sock.recvfrom(256)
#	print('received')
#	for event in pygame.event.get(): # User did something

#		if event.type == pygame.QUIT: # If user clicked close

#			done = True # Flag that we are done so we exit this loop

	
pygame.quit()
quit()
