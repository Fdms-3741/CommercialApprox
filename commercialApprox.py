import numpy as np

class CommercialValueApproximator:
    
    # Gives tolerances and numbers each series
    tolerances = {6:(0.2,),12:(0.1,),24:(0.05,0.01),48:(0.02,),96:(0.01,),192:(0.005,0.0025,0.001)}

    def __init__(self,custom=None):
        """ 
        Initializes and calculates the values for each series
        """
        self.series = {}
            
        # Calculates the significant digits 
        for i  in self.tolerances.keys():
            values = [1]
            for j in range(i):
                values.append(values[-1]*10**(1/i))
            values = values[:-1]
            # Gives extra digits in order to acommodate higher tolerances
            minTol = -np.floor(np.log10(min(self.tolerances[i])))
            
            # Rounds to the significant digits
            values = np.array(values)*(10**minTol)
            values = np.round(values)/(10**minTol)
        
            # Attributes them to their respective series
            self.series[i] = values
        
        if custom:
            self.tolerances['custom'] = (0.00001,)
            self.series['custom'] = np.array(custom)


    def _Approx(self,value,floor=True,series=12,checkEqual=True):
        """ 
        Aproximates the value to the nearest commercial standard
        floor (bool) - If true, rounds down to the nearest value. If false, rounds up
        series - Selects the appropiate series
        """
        
        if 'custom' in self.series.keys():
            series='custom'

        magn = np.floor(np.log10(value))

        # Aligns magnitude with generated table
        orderMatch = value/(10**magn)

        # Matches distance with 
        distance = self.series[series] - orderMatch
        
        # Will round bel
        if checkEqual:
            # Considers equal if less than 10% than minimum tolerance
            equalityCheck = np.less(np.abs(distance),np.ones(distance.shape)*0.1*min(self.tolerances[series]))
            
            # Imediately returns if value already is commercial (by the earlier approximation)
            if np.any(equalityCheck):
                return (self.series[series][np.where(equalityCheck)]*(10**magn))[0]
                
        try:
            value = self.series[series][distance<0][-1] if floor else self.series[series][distance>0][0]
        except IndexError:
            if floor:
                #value = self.series[series][-1]/10 if (np.abs(orderMatch-self.series[series][0]) < np.abs(orderMatch*10-self.series[series][-1])) else self.series[series][0]
                value = self.series[series][-1]/10 
            else:
                #value = self.series[series][0]*10 if ((np.abs(orderMatch-self.series[series][-1]) < np.abs(orderMatch/10-self.series[series][0]))) else self.series[series][-1]
                value = self.series[series][0]*10 

        return value*10**magn

    def Upper(self,value,series=12,checkEqual=False):
        """
        Approximates for the nearest upper commercial values 
        """
        return self._Approx(value,floor=False,series=series,checkEqual=checkEqual)
    
    def Lower(self,value,series=12,checkEqual=False):
        """
        Approximates to the nearest lower commercial values
        """
        return self._Approx(value,floor=True,series=series,checkEqual=checkEqual)
    

    def Approx(self,value,series=12):
        """
        Approximates to the nearest commercial values
        """
        return self.Lower(value,checkEqual=True) if (np.abs(self.Lower(value,checkEqual=True)-value) < np.abs(self.Upper(value,checkEqual=True)-value)) else self.Upper(value,checkEqual=True)

if __name__ == "__main__":
    # Testing module
    approx = CommercialValueApproximator()

    values = [131,44.345,2345,765.67,64546664,4567765,345,21,1,34,0.8,55.777,9,1.8,2.2,2.1,2.3]

    print()
    for i in values:
        print(f'Exact: {i} / Upper: {approx.Upper(i)} / Approx: {approx.Approx(i)} / Lower: {approx.Lower(i)}')
        print()

    print("Trying to step down value by multiple calls")
    val = 1843
    print(f"{val} -> ",end='')
    for i in range(15):
        val = approx.Lower(val)
        print(f"{val} -> ",end='')
    print()
    print()
    
    print("Trying to step up value by multiple calls")
    val = 1874
    print(f"{val} -> ",end='')
    for i in range(15):
        val = approx.Upper(val)
        print(f"{val} -> ",end='')
    print()
    print()
    
    del approx
    approx = CommercialValueApproximator([1,2,3,5,7])
    print()
    for i in values:
        print(f'Exact: {i} / Upper: {approx.Upper(i)} / Approx: {approx.Approx(i)} / Lower: {approx.Lower(i)}')
        print()

    
