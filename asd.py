import csv
import matplotlib.pyplot as plt
import numpy as np



# Load the CSV file
file_path = "/Users/tony/Documents/EDUCATION/project/bitcoin1.csv"

# Read all lines into a list
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

start = 100  # Remove elements from index 1 to 3 (exclusive)
del data[start:]
del data[0]

priceEstimates = []
priceMean = 0

for i in data:
    priceEstimates.append((float(i[2])+float(i[3]))/2)

for i in priceEstimates:
    priceMean += i
priceMean = priceMean / len(priceEstimates)

i = 0
sumForCor1 = 0
sumForCor2 = 0
while i < len(priceEstimates) - 1:
    sumForCor1 += (priceEstimates[i]-priceMean)*(priceEstimates[i+1] - priceMean)
    sumForCor2 += (priceEstimates[i]-priceMean)*(priceEstimates[i]-priceMean)
    i += 1

    
autoCorr = sumForCor1/sumForCor2
# print(autoCorr)

estimatedPricesAR1 = []

for i in priceEstimates:
    estimatedPricesAR1.append(i * autoCorr)



j = 0
sumForCor3 = 0
sumForCor4 = 0
sumForCor5= 0
while j < len(priceEstimates) - 2:
    sumForCor3 += (priceEstimates[j]*priceEstimates[j+2])
    sumForCor5 -= autoCorr*(priceEstimates[j]*priceEstimates[j+2])
    sumForCor4 += priceEstimates[j+2]*priceEstimates[j+2]
    j += 2

    
autoCorr1 = (sumForCor3+sumForCor5)/sumForCor4
phiEstimate1 = (autoCorr1-autoCorr*autoCorr)/(1-autoCorr*autoCorr)
# print(autoCorr1)

estimatedPricesAR2 = []
i = 0
while i < len(priceEstimates)-1:
    estimatedPricesAR2.append((autoCorr * priceEstimates[i] + autoCorr1 * priceEstimates[i+1]))
    i += 1


#AR(2): Yt = autoCorr Y(t-1)+  autoCorr1 Y(t-2) + et


# ARMA(1,1) model

residAnalysis = []

i = 0
while i < len(estimatedPricesAR1):
    residAnalysis.append(priceEstimates[i] - estimatedPricesAR1[i])
    i += 1

#Calculating tetta

i = 0
tettaNum = 0
tettaDenum = 0
while i < len(residAnalysis)-1:
    tettaNum += residAnalysis[i]* residAnalysis[i+1]
    tettaDenum += residAnalysis[i+1]*residAnalysis[i+1]
    i+=1

tetta = tettaNum/tettaDenum
estimatedPricesARMA = []

i = 0
while i < len(priceEstimates)-1:
    estimatedPricesARMA.append((autoCorr * priceEstimates[i] + tetta * residAnalysis[i+1]) + residAnalysis[i])
    i += 1
estimatedPricesARMA.append(31932)

asd = [
]
i = 0
while i < len(priceEstimates):

    asd.append(i)
    i += 1
# print(tetta)


# print(priceEstimates)
# print(len(priceEstimates))


# print(estimatedPricesAR1)
# print(len(estimatedPricesAR1))

# print(estimatedPricesAR2)
# print(len(estimatedPricesAR2))


# print(estimatedPricesARMA)
# print(len(estimatedPricesARMA))



# Create data for the first graph
x1 = asd
y1 = priceEstimates


# Create data for the second graph
x2 = asd
y2 = estimatedPricesARMA


# Plot both graphs on the same axis
plt.plot(x1, y1, label='True prices')  # First graph
plt.plot(x2, y2, label='ARMA estimates')  # Second graph

# Add labels, title, and legend
plt.xlabel('Time')
plt.ylabel('Bitcoin Price')
plt.title('True prices and ARMA comparison')
plt.legend()

# Show the plot
plt.show()
