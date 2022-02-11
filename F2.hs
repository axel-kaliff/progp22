module F2 where
import Data.List

---- 2 Molekylära sekvenser ----

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

seqType :: MolSeq -> SeqType
seqType (MolSeq _ _ seqtype) = seqtype


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

---- 3 Profiler och sekvenser ----

nucleotides = "ACGT"
aminoacids = "ARNDCEQGHILKMFPSTWYV"

makeProfileMatrix :: [MolSeq] -> [[(Char, Int)]]
makeProfileMatrix [] = error "Empty sequence list"
makeProfileMatrix sl = res
   where
      -- Evaluates sequence type from head of sequence list
      t = seqType (head sl)

      -- creates a list of tuples of each nucleotide/aminoacid (depending on type) and a 0
      -- e.g. for dna: defaults = [('A',0),('C',0),('G',0),('T',0)]
      defaults =     
         if (t == DNA) then
            zip nucleotides (replicate (length nucleotides) 0) -- Rad (i)
         else
            zip aminoacids (replicate (length aminoacids) 0) -- Rad (ii)
   
      -- extracts sequences from input and puts in list 'strs'
      strs = map seqSequence sl -- Rad (iii)
      
      -- Counts the number of each nucleotide/aminoacid in each position
      tmp1 = map (map (\x -> ((head x), (length x))) . group . sort) (transpose strs) -- Rad (iv)
      equalFst a b = (fst a) == (fst b)
      res = map sort (map (\l -> unionBy equalFst l defaults) tmp1)

data Profile = Profile {name :: String, matrix :: [[(Char, Int)]], sequencType :: SeqType, numOfSeqs :: Int}

molseqs2profile :: String -> [MolSeq] -> Profile
molseqs2profile s mols 
   | isDNA (seqSequence (head mols)) = Profile s (makeProfileMatrix mols) DNA (length mols)
   | otherwise = Profile s (makeProfileMatrix mols) Protein (length mols)

profileName :: Profile -> String
profileName (Profile name _ _ _) = name

profileMatrix :: Profile -> [[(Char, Int)]]
profileMatrix (Profile _ matrix _ _) = matrix

profileType :: Profile -> SeqType
profileType (Profile _ _ sequenceType _) = sequenceType

profileFrequency :: Profile -> Int -> Char -> Double
profileFrequency (Profile _ matrix _ num) index char = (fromIntegral (snd (head (filter (\x -> fst x == char) (matrix !! index))))) / (fromIntegral num)

profileSeqLength :: Profile -> Int
profileSeqLength (Profile _ matrix _ _) = length matrix

profileDistance :: Profile -> Profile -> Double
profileDistance profile1 profile2
    | profileType profile1  == DNA = sum [abs ((profileFrequency profile1 x y) - (profileFrequency profile2 x y) )| y <- nucleotides, x <- [0..(profileSeqLength profile1)-1]]
    | otherwise = sum [abs ((profileFrequency profile1 x y) - (profileFrequency profile2 x y) )| y <- aminoacids, x <- [0..(profileSeqLength profile1)-1]]

