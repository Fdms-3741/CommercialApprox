import numpy as np

class CommercialValueApproximator:
    
    # Gives tolerances and numbers each series
    tolerances = {6:(0.2,),12:(0.1,),24:(0.05,0.01),48:(0.02,),96:(0.01,),192:(0.005,0.0025,0.001)}

    def __init__(self):
        """ 
        Initializes and calculates the values for each series
        """
        self.series = {}
            
        # Calculates the significant digits 
        for i  in self.tolerances.keys():
            values = [1]
            for j in range(i):
                values.append(values[-1]*10**(1/i))
                
            # Gives extra digits in order to acommodate higher tolerances
            minTol = -np.floor(np.log10(min(self.tolerances[i])))
            
            # Rounds to the significant digits
            values = np.array(values)*(10**minTol)
            values = np.round(values)/(10**minTol)
        
            # Attributes them to their respective series
            self.series[i] = values

    def Approx(self,value,floor=True,series=12):
        """ 
        Aproximates the value to the nearest commercial standard
        floor (bool) - If true, rounds down to the nearest value. If false, rounds up
        series - Selects the appropiate series
        """

        magn = np.floor(np.log10(value))

        # Aligns magnitude with generated table
        orderMatch = value/(10**magn)

        # Matches distance with 
        distance = self.series[series] - orderMatch
        
        try:
            value = self.series[series][distance<0][-1] if floor else self.series[series][distance>0][0]
        except IndexError:
            if floor:
                value = self.series[series][-1]/10 if (np.abs(orderMatch-self.series[series][0]) < np.abs(orderMatch*10-self.series[series][-1])) else self.series[series][0]
            else:
                value = self.series[series][0]*10 if ((np.abs(orderMatch-self.series[series][-1]) < np.abs(orderMatch/10-self.series[series][0]))) else self.series[series][-1]

        return value*10**magn

    def Upper(self,value,series=12):
        """
        Approximates for the nearest upper commercial values 
        """
        return self.Approx(value,floor=False,series=series)
    
    def Lower(self,value,series=12):
        """
        Approximates to the nearest lower commercial values
        """
        return self.Approx(value,floor=True,series=series)
    
if __name__ == "__main__":
    # Testing module
    approx = CommercialValueApproximator()

    values = [131,44.345,2345,765.67,64546664,4567765,345,21,1,34,0.8,55.777,9]

    print()
    for i in values:
        print(f'Exact: {i} / Upper: {approx.Upper(i)} / Lower: {approx.Lower(i)}')
        print()
