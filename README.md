# CommercialApprox
Simple Python Package that rounds arbitrary values to the nearest E-Series preferred values. 
Those values are commonly seen in commercial resistors and capacitors.

## Disclaimer

This is only an approximation. The resistor and capacitors values highly depend on their availability at your local stores.
The values are generated following the IEC 60063:2015 standard that not necessarily is practiced by all producers.

## Usage

The package contains a single class that is responsible to generating the E-Series tables every run. 

Here's an example code:

```python3

a = CommercialValueApproximator()

val = 11312

a.Approx(val) # -> Gives the best approximation 
a.Upper(val)  # -> Gives the best upper approximation
a.Lower(val)  # -> Gives the best lower approximation
```

In case there's the need to select even lower values based on a starting value, the Lower and Upper function can be chained to swipe the existing values.

For example, the following code:

```python3
print("Trying to step down value by multiple calls")
val = 1874
print(f"{val} -> ",end='')
for i in range(14):
    val = a.Lower(val) # <- multiple calls on the already approximated value
    print(f"{val} -> ",end='')
print(a.Lower(val))
print()
```

Will produce the output:
```
Trying to step down value by multiple calls
1843 -> 1800.0 -> 1500.0 -> 1200.0 -> 1000.0 -> 830.0000000000001 -> 680.0 -> 560.0 -> 459.99999999999994 -> 380.0 -> 320.0 -> 260.0 -> 220.00000000000003 -> 180.0 -> 150.0 -> 120.0 
```
This method wont work when using the Approx method.
