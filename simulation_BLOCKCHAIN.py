import hashlib


class Block:                                                     # A Block Structure
	def __init__(self, number, nonce, data, prevHash, hash):
		self.number = number
		self.nonce = nonce
		self.data = data
		self.prevHash = prevHash
		self.hash = hash

	def getValues(self):
		d = dict()
		d['Number'] = self.number
		d['Nonce'] = self.nonce
		d['Data'] = self.data
		d['PrevHash'] = self.prevHash
		d['Hash'] = self.hash

		return d


class BlockChain:                                               # A Block Chain
	def __init__(self):
		self.chain = []
		self.proofOfWork_Prefix = "0000"                        # ProofOfWork - Leading zeros
		self.proofOfWork_PrefixLength = 4


	def addNewBlock(self, data):                                # New Block
		numberOfBlocksInChain = len(self.chain)

		if numberOfBlocksInChain == 0:
			prevHash = 0
		else:
			prevHash = self.chain[numberOfBlocksInChain - 1]['Hash']

		nonce = 0

		hashval = hashlib.sha256(str(data).encode('utf-8')).hexdigest()

		block = Block(numberOfBlocksInChain, nonce, data, prevHash, hashval)

		self.chain.append(block.getValues())


	def printBlockChain(self):
		print(*self.chain, sep = "\n")


	def updateData(self, blocknumber, data):                    # Update Data and Hash Value accordingly
		self.chain[blocknumber]['Data'] = data                  # New Hash value genearted using Nonce and Data
		self.chain[blocknumber]['Hash'] = hashlib.sha256(str(str(self.chain[blocknumber]['Nonce']) + str(self.chain[blocknumber]['Data'])).encode('utf-8')).hexdigest()


	def mineChain(self):                                       # Check if any block in chain is updated
		numberOfBlocksInChain = len(self.chain)

		updatedAnyBlock = False

		i = 0
		while i < numberOfBlocksInChain:                       # Proof of work will validate it
			if self.chain[i]['Hash'][0:self.proofOfWork_PrefixLength] != self.proofOfWork_Prefix:
				updatedAnyBlock = True
				break

			i+=1

		if updatedAnyBlock:
			for d in range(i,numberOfBlocksInChain,1):
				self.mineBlock(self.chain[d])


	def mineBlock(self, dictOfBlock):                          # Update block to satisfy Proof of Work

		numberOfBlocksInChain = len(self.chain)

		blocknumber = dictOfBlock['Number']
		nonce = dictOfBlock['Nonce']
		data = dictOfBlock['Data']
		newHash = hashlib.sha256(str(str(nonce) + str(data)).encode('utf-8')).hexdigest()

		while newHash[0:self.proofOfWork_PrefixLength] != self.proofOfWork_Prefix:
			nonce += 1
			newHash = hashlib.sha256(str(str(nonce) + str(data)).encode('utf-8')).hexdigest()

		self.chain[blocknumber]['Nonce'] = nonce
		self.chain[blocknumber]['Hash'] = newHash

		if blocknumber < numberOfBlocksInChain - 1:
			self.chain[blocknumber + 1]['PrevHash'] = newHash


