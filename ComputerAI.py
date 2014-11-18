#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import time
import math

class PlayerAI(BaseAI):
	def getMove(self, grid):
		
		StartTime=time.time()
		MinMax=0
		MaxDepth=6

		# DFS Algorithm
		# Initialization of variables
		InitialGrid=grid
		if MinMax:
			InitialMoves=grid.getAvailableMoves()
		else:
			InitialMoves=grid.getAvailableCells()

		NodesList=[InitialGrid] # List of all the nodes (stores the grid)	

		ParentsList=[-1]		# For each node, indicates who is its parent node

		SonsList=[]  			# List of lists, for each node it stores a list with its sons
		SonsList.insert(0, InitialMoves)

		IterationList=[1]		# For each node, it stores which one of the "sons" we have already explored and which is the next to cover

		if MinMax:
			(Alpha,Beta,Value)=([float('-inf')],[float('inf')],[float('-inf')])
		else:
			(Alpha,Beta,Value)=([float('-inf')],[float('inf')],[float('inf')])
			
		NodeDepth=[0]

		CurrentNode=0
		SolutionNode=1
		CurrentOptions=InitialMoves
		ContinueIteration=1
		OptionValue=[]

		CurrentGrid=InitialGrid.clone()
		
		# Build the decision tree
		while ContinueIteration:
			# Update variables
			Depth=NodeDepth[CurrentNode]

			if IterationList[CurrentNode]<=len(SonsList[CurrentNode]) and Depth<MaxDepth:  # If we have not reached the bottom of this branch, continue going down
				# Advance to the next node
				Parent=CurrentNode
				LastNode=len(NodesList)-1
				CurrentNode=LastNode+1
				NextIteration=IterationList[Parent]   # Which one of the sons is the next to go
				Move=SonsList[Parent][NextIteration-1]
				IterationList[Parent]=IterationList[Parent]+1
				#Update node values in data structures
				ParentsList.append(Parent)
				IterationList.append(1)
				NodeDepth.append(Depth+1)
				Alpha.append(Alpha[Parent])
				Beta.append(Beta[Parent])
				# Update the grid for current node
				CurrentGrid=NodesList[Parent].clone()
				if NodeDepth[CurrentNode] % 2 == MinMax:
					CurrentGrid.move(Move)
					Value.append(float('inf'))
				else:
					CurrentGrid.setCellValue(Move,2)
					Value.append(float('-inf'))
				NodesList.append(CurrentGrid)
				# Determine available options
				if NodeDepth[CurrentNode] % 2 == MinMax:
					CurrentOptions=CurrentGrid.getAvailableCells()
				else:
					CurrentOptions=CurrentGrid.getAvailableMoves()
				SonsList.append(CurrentOptions)

			else:   # We have reached the end of a branch and have to go up until we find a node that has sons we have not explored
				# Update the value of the node
				Value[CurrentNode]=self.Utility(NodesList[CurrentNode])
				# Update alpha/beta/Value of the parent node
				if NodeDepth[CurrentNode] % 2 == MinMax:
					Value[ParentsList[CurrentNode]]=max(Value[ParentsList[CurrentNode]],Value[CurrentNode])
					if Value[ParentsList[CurrentNode]]>=Beta[ParentsList[CurrentNode]]:
						IterationList[ParentsList[CurrentNode]]=len(SonsList[ParentsList[CurrentNode]])+1
					Alpha[ParentsList[CurrentNode]]=max(Alpha[ParentsList[CurrentNode]],Value[ParentsList[CurrentNode]])
				else:
					Value[ParentsList[CurrentNode]]=min(Value[ParentsList[CurrentNode]],Value[CurrentNode])
					if Value[ParentsList[CurrentNode]]<=Alpha[ParentsList[CurrentNode]]:
						IterationList[ParentsList[CurrentNode]]=len(SonsList[ParentsList[CurrentNode]])+1
					Beta[ParentsList[CurrentNode]]=min(Beta[ParentsList[CurrentNode]],Value[ParentsList[CurrentNode]])
				
				FoundNode=0   # Controls the iteration (Found a node that still has a branch to explore)
				while not(FoundNode):
					CurrentNode=ParentsList[CurrentNode]  # Move up to the parent node
					
					# If this pruned (bc of alpha-beta or bc it is complete)
					if IterationList[CurrentNode]>len(SonsList[CurrentNode]):
						# Update alpha/beta/Value of the parent node
						if NodeDepth[CurrentNode] % 2 == MinMax:
							Value[ParentsList[CurrentNode]]=max(Value[ParentsList[CurrentNode]],Value[CurrentNode])
# 							if ParentsList[CurrentNode]==0 and Value[ParentsList[CurrentNode]]<Value[CurrentNode]:
# 								SolutionNode=CurrentNode
							if Value[ParentsList[CurrentNode]]>=Beta[ParentsList[CurrentNode]]:
								IterationList[ParentsList[CurrentNode]]=len(SonsList[ParentsList[CurrentNode]])+1
							Alpha[ParentsList[CurrentNode]]=max(Alpha[ParentsList[CurrentNode]],Value[ParentsList[CurrentNode]])
						else:
							Value[ParentsList[CurrentNode]]=min(Value[ParentsList[CurrentNode]],Value[CurrentNode])
# 							if ParentsList[CurrentNode]==0 and Value[ParentsList[CurrentNode]]>Value[CurrentNode]:
# 								SolutionNode=CurrentNode
							if Value[ParentsList[CurrentNode]]<=Alpha[ParentsList[CurrentNode]]:
								IterationList[ParentsList[CurrentNode]]=len(SonsList[ParentsList[CurrentNode]])+1
							Beta[ParentsList[CurrentNode]]=min(Beta[ParentsList[CurrentNode]],Value[ParentsList[CurrentNode]])
						# Record Solution if we are in the first level
						if ParentsList[CurrentNode]==0:
							OptionValue.append(Value[CurrentNode])
						# Kill if we have covered the entire tree
						if ParentsList[CurrentNode]==-1 and FoundNode==0:	  
							ContinueIteration=0
							break
					else:    # The node still has available sons to explore
						FoundNode=1
							
# 		OptimalMove=InitialMoves[SolutionNode-1]
		
		EndTime=time.time()
		ElapsedTime=EndTime-StartTime
		print ElapsedTime
		a=len(InitialMoves)
		print Value[1:a+1]
		
		Optimal=Value[0]
		Node=OptionValue.index(Optimal)
		OptimalMove=InitialMoves[Node]
		
# 		#TEST
# 		InitialUtility=self.Utility(InitialGrid)
# 		InitialUtility2=self.Utility2(InitialGrid)
# 		print InitialUtility, ' - ', InitialUtility2, ' = ', InitialUtility-InitialUtility2
				

# 		moves = grid.getAvailableMoves()
		return OptimalMove # if OptimalMove else None
	
	# Utility Function
	def Utility(self,grid):
		# Optimize order of tiles
		Size=grid.size-1
		MaxTile=grid.getMaxTile()
		Factor=0.5
		TileUtility=0
		MergeBonus=0
		CloseBonus=0
# 		ProximityBonus=0
		UPUtility=[0]*grid.size
		DOWNUtility=[0]*grid.size
		LEFTUtility=[0]*grid.size
		RIGHTUtility=[0]*grid.size
		
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				Value=grid.map[x][y]
				TileUtility=self.UtilityTile(Value)
				UPUtility[y]=UPUtility[y]+TileUtility
				DOWNUtility[y]=DOWNUtility[y]+TileUtility
				LEFTUtility[x]=LEFTUtility[x]+TileUtility
				RIGHTUtility[x]=RIGHTUtility[x]+TileUtility
				# UP adjustments
				if x<Size and grid.map[x+1][y]>Value:
					UPUtility[y]=UPUtility[y]-self.Penalization(grid.map[x+1][y],Value,MaxTile)
				elif x<Size and grid.map[x+1][y]<=Value and Value>2:
					CloseBonus=self.Bonus(Value,grid.map[x+1][y],MaxTile,Factor)
				# DOWN adjustments
				if x>0 and grid.map[x-1][y]>Value:
					DOWNUtility[y]=DOWNUtility[y]-self.Penalization(grid.map[x-1][y],Value,MaxTile)
				elif x>0 and grid.map[x-1][y]<=Value and Value>2:
					CloseBonus=self.Bonus(Value,grid.map[x-1][y],MaxTile,Factor)
				# RIGHT adjustments
				if y<Size and grid.map[x][y+1]>Value:
					RIGHTUtility[x]=RIGHTUtility[x]-self.Penalization(grid.map[x][y+1],Value,MaxTile)
				elif y<Size and grid.map[x][y+1]<=Value and Value>2:
					CloseBonus=self.Bonus(Value,grid.map[x][y+1],MaxTile,Factor)
				# LEFT adjustments
				if y>0 and grid.map[x][y-1]>Value:
					LEFTUtility[x]=LEFTUtility[x]-self.Penalization(grid.map[x][y-1],Value,MaxTile)
				elif y>0 and grid.map[x][y-1]<=Value and Value>2:
					CloseBonus=self.Bonus(Value,grid.map[x][y-1],MaxTile,Factor)
				
		# Aggregate Utilities
		UPDOWNUtility=0
		LEFTRIGHTUtility=0
		for i in xrange(grid.size):
			UPDOWNUtility=UPDOWNUtility+max(UPUtility[i],DOWNUtility[i])
			LEFTRIGHTUtility=LEFTRIGHTUtility+max(LEFTUtility[i],RIGHTUtility[i])
		Utility=(UPDOWNUtility+LEFTRIGHTUtility)/2
		
# 		# Penalization for having too few empty cells
# 		AvailableCells=len(grid.getAvailableCells())
# 		EmptyCells=0
# 		if AvailableCells<>0 and AvailableCells<4:
# 			EmptyCells=int(Utility/AvailableCells)
		
		# Total Utility
		Utility=Utility+CloseBonus#+MergeBonus-EmptyCells
		return Utility
	
	# Tile Utility Function
	def UtilityTile(self,Value):
		if Value==0:
			Utility=0
		else:
			Utility=int((math.log(Value)/math.log(2)-1)*Value)
		return Utility
	
	# Penalization Utility Function
	def Penalization(self,ValueMax,ValueMin,MaxTile):
		#Penalization=int((math.log(ValueMax-ValueMin)/math.log(2)-1)*(ValueMax-ValueMin))
		Penalization=self.UtilityTile(ValueMax)-self.UtilityTile(ValueMin)
# 		if ValueMin==0 and MaxTile>=1024:
# 			Penalization=0
		return Penalization
	
	# Bonus Function
	def Bonus(self,ValueMax,ValueMin,MaxTile,Factor):
		# Better reliability until the 1024 tile
# 		if MaxTile<1024:
# 			Bonus=0
# 		else:
		Bonus=Factor*self.UtilityTile(ValueMin)**2/self.UtilityTile(ValueMax)
		return Bonus