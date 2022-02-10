data MolSeq = MolSeq {sequenceName:: String, sequence :: String, sequenceType :: SeqType} deriving (Show, Eq)

string2seq :: String -> String -> MolSeq
string2seq seqName sequence 
   | isDNA sequence = MolSeq seqName sequence DNA
   | otherwise = MolSeq seqName sequence Protein

isDNA :: String -> Bool

isDNA [] = True
isDNA (x:xs)
   | x `elem` "AGCT" = isDNA xs
   | otherwise = False 

seqName :: MolSeq -> String
seqName (MolSeq name _ _) = name 

seqSequence :: MolSeq -> String
seqSequence (MolSeq _ sequence _) = sequence 

seqLength :: MolSeq -> Int
seqLength (MolSeq _ sequence _) = length sequence 


data SeqType = DNA | Protein deriving(Eq, Show)

seqDistance :: MolSeq -> MolSeq -> Double 
seqDistance mol1 mol2
   | sequenceType mol1 /= sequenceType mol2 = error "Impossible to compare DNA and Protein" 
   | sequenceType mol1 == DNA && sequenceType mol2 == DNA = jukesCantor mol1 mol2
   | otherwise = poissonModel mol1 mol2 -- Protein 

jukesCantor :: MolSeq -> MolSeq -> Double
jukesCantor mol1 mol2
   | alpha mol1 mol2 > 0.74 = 3.3
   | otherwise  = (-3/4)*log(1-((4/3)*alpha mol1 mol2))

poissonModel :: MolSeq -> MolSeq -> Double 
poissonModel mol1 mol2 
   | alpha mol1 mol2 <= 0.94 = (-19/20)*log(1-((20/19)*alpha mol1 mol2)) 
   | otherwise = 3.7

alpha :: MolSeq -> MolSeq -> Double 
alpha mol1 mol2 = fromIntegral(hammingDistance(seqSequence mol1) (seqSequence mol2)) / fromIntegral(seqLength mol1)

hammingDistance :: String -> String -> Int  
hammingDistance [] [] = 0
hammingDistance x1 x2 
   | head x1 == head x2 = hammingDistance (tail x1) (tail x2)
   | otherwise = 1 + hammingDistance (tail x1) (tail x2)

