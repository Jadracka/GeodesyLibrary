# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:45:14 2021

@author: schloe
@saboteur: jbar
"""

import math


class Angle:
    T_RAD = 0
    T_GON = 1
    T_DEG = 2
    T_SELF_DEFINED = 3

    # Internal constants
    __INTERNAL_MINIMUM = -math.pi
    __INTERNAL_MAXIMUM = math.pi
    __INTERNAL_INTERVAL = 2 * math.pi  # tau
    __INTERNAL_HALF_INTERVAL = math.pi

    def __init__(self, angle=0, angle_type=T_RAD, symmetric=False, minimum=0, maximum=2 * math.pi):
        # Type validations
        if not isinstance(angle, (float, int)):
            raise TypeError("The angle must be a float or int.")
        if not isinstance(symmetric, bool):
            raise TypeError("The symmetric flag must be a boolean.")
        if not isinstance(minimum, (float, int)) or not isinstance(maximum, (float, int)):
            raise TypeError("Minimum and maximum values must be float or int.")
        if angle_type not in [self.T_RAD, self.T_GON, self.T_DEG, self.T_SELF_DEFINED]:
            raise ValueError("Invalid angle type. Use T_RAD, T_GON, T_DEG, or T_SELF_DEFINED.")

        # Interval initialization
        self.angle_type = angle_type
        self.is_symmetric = symmetric

        if angle_type == self.T_SELF_DEFINED:
            self.minimum = minimum
            self.maximum = maximum
        else:
            self.minimum = 0
            if angle_type == self.T_RAD:
                self.maximum = 2 * math.pi
            elif angle_type == self.T_GON:
                self.maximum = 400
            elif angle_type == self.T_DEG:
                self.maximum = 360
            else:
                raise ValueError("Unexpected angle type.")

        self.interval = self.maximum - self.minimum
        self.half_interval = self.interval / 2

        if symmetric and angle_type != self.T_SELF_DEFINED:
            self.minimum -= self.half_interval
            self.maximum -= self.half_interval

        self.angle = self._external_to_internal(self._normalize(angle))

    def __str__(self):
        return f"{self._normalize(self._internal_to_external(self.angle))}"

    # Internal normalization to range
    def _normalize(self, angle):
        if angle < self.minimum or angle >= self.maximum:
            return (angle - self.minimum) % self.interval + self.minimum
        return angle

    # Convert external angle to internal representation
    def _external_to_internal(self, value):
        return value / self.half_interval * self.__INTERNAL_HALF_INTERVAL

    # Convert internal angle to external representation
    def _internal_to_external(self, value):
        return self._normalize(value * self.half_interval / self.__INTERNAL_HALF_INTERVAL)

    # Arithmetic operations
    def __add__(self, other):
        if isinstance(other, Angle):
            angle = self.angle + other.angle
        elif isinstance(other, (float, int)):
            angle = self.angle + self._external_to_internal(other)
        elif isinstance(other, str) and other.strip().replace('.', '', 1).isdigit():
            angle = self.angle + self._external_to_internal(float(other))
        else:
            raise TypeError("Addition only supports Angle, float, int, or numeric strings.")
        return self._internal_to_external(angle)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Angle):
            angle = self.angle - other.angle
        elif isinstance(other, (float, int)):
            angle = self.angle - self._external_to_internal(other)
        elif isinstance(other, str) and other.strip().replace('.', '', 1).isdigit():
            angle = self.angle - self._external_to_internal(float(other))
        else:
            raise TypeError("Subtraction only supports Angle, float, int, or numeric strings.")
        return self._internal_to_external(angle)

    def __rsub__(self, other):
        if isinstance(other, (float, int)):
            angle = self._external_to_internal(other) - self.angle
            return self._internal_to_external(angle)
        elif isinstance(other, str) and other.strip().replace('.', '', 1).isdigit():
            angle = self._external_to_internal(float(other)) - self.angle
            return self._internal_to_external(angle)
        else:
            raise TypeError("Subtraction only supports float, int, or numeric strings.")


    def __mul__(self, factor):
        if isinstance(factor, (float, int)):
            return self._internal_to_external(self.angle * factor)
        elif isinstance(factor, Angle):
            # Multiply internal representations of the angles
            return self._internal_to_external(self.angle * factor.angle / self.__INTERNAL_INTERVAL)
        else:
            raise TypeError("Multiplication only supports Angle, float, or int.")

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __truediv__(self, divisor):
        if isinstance(divisor, (float, int)):
            if divisor == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            return self._internal_to_external(self.angle / divisor)
        elif isinstance(divisor, Angle):
            if divisor.angle == 0:
                raise ZeroDivisionError("Division by an angle with value zero is undefined.")
            # Return the ratio of the two angles
            return self.angle / divisor.angle
        else:
            raise TypeError("Division only supports Angle, float, or int.")
    
    def __rtruediv__(self, other):
        if isinstance(other, (float, int)):
            if self.angle == 0:
                raise ZeroDivisionError("Cannot divide by an angle with a value of zero.")
            return other / self._internal_to_external(self.angle)
        else:
            raise TypeError("Reverse division only supports float or int.")

    def __neg__(self):
        return -self._internal_to_external(self.angle)

    def __invert__(self):
        return self._internal_to_external(self.angle)

    # Comparisons
    def __lt__(self, other):
        if not isinstance(other, Angle):
            raise TypeError("Angles can only be compared to other Angles.")
        return self._normalize(self.angle - other.angle) < 0

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        if not isinstance(other, Angle):
            return False
        return math.isclose(self.angle, other.angle, rel_tol=1e-9)

    def __ne__(self, other):
        return not self == other

    # Static trigonometric methods
    @staticmethod
    def sin(value):
        return math.sin(value.angle if isinstance(value, Angle) else value)

    @staticmethod
    def cos(value):
        return math.cos(value.angle if isinstance(value, Angle) else value)

    @staticmethod
    def tan(value):
        return math.tan(value.angle if isinstance(value, Angle) else value)

    # Inverse trigonometric functions
    @staticmethod
    def asin(value):
        if not -1 <= value <= 1:
            raise ValueError("asin() domain is -1 <= value <= 1.")
        return math.asin(value)

    @staticmethod
    def acos(value):
        if not -1 <= value <= 1:
            raise ValueError("acos() domain is -1 <= value <= 1.")
        return math.acos(value)

    @staticmethod
    def atan(value):
        return math.atan(value)

    @staticmethod
    def atan2(self, arg1, arg2, angle_type=None, symmetric=None):
        if not isinstance(arg1, (float, int)) or not isinstance(arg2, (float, int)):
            raise TypeError("Arguments for atan2 must be float or int.")
        
        # Use the instance's current configuration if type and symmetric are not provided
        angle_type = angle_type if angle_type is not None else self.angle_type
        symmetric = symmetric if symmetric is not None else self.is_symmetric
        
        self.__init__(0, angle_type, symmetric)  # Reinitialize using existing properties
        self.angle = math.atan2(arg1, arg2)
        return self._internal_to_external(self.angle)

    @staticmethod
    def is_similar(angle1, angle2, tolerance):
        return abs(angle1 - angle2) < tolerance

      
        
        
w1=Angle(500,Angle.T_GON)
w2=Angle(200,Angle.T_GON)
w3=Angle(50,Angle.T_GON)
w4=Angle(0,Angle.T_DEG)
w4=w4+720

print('w4      =',w4)
print('w1      =',w1)
print('-w1      =',-w1)
print('~w1     =',~w1)
print('w2      =',w2)
print('w1+w2   =',w1+w2)
print('w1+30   =',w1+30)
print('w1+30.0 =',w1+30.0)
#print('w1+\'30\' =',w1+'30')
print('30+w1   =',30+w1)
print('30.0+w1 =',30.0+w1)
#print('\'30\'+w1 =','30'+w1)
print('w2-w1   =',w2-w1)
print('w1-30   =',w1-30)
print('w1-30.0 =',w1-30.0)
#print('w1-\'30\' =',w1-'30')
print('30-w1   =',30-w1)
print('30.0-w1 =',30.0-w1)
#print('\'30\'-w1 =','30'-w1)
print('w1*w2   =',w1*w2)
print('w1*3    =',w1*3)
print('w1*3.0  =',w1*3.0)
print('3*w1    =',3*w1)
print('-3.0*w1 =',-3.0*w1)
print('w1/3    =',w1/3)
print('3/w1    =',3/w1)
print('w1/0    = division by zero error')
print('sin(w1) =',Angle.sin(w1))
#print('atan2(-3,2)=',w3.atan2(-3,2,Angle.T_GON))
print('20<19   =',Angle(20,Angle.T_GON)<Angle(19,Angle.T_GON))
print('19<20   =',Angle(19,Angle.T_GON)<Angle(20,Angle.T_GON))
print('19<19   =',Angle(19,Angle.T_GON)<Angle(19,Angle.T_GON))
print('19<=19  =',Angle(19,Angle.T_GON)<=Angle(19,Angle.T_GON))
print('50<251  =',Angle(50,Angle.T_GON)<Angle(251,Angle.T_GON))
print('50<250  =',Angle(50,Angle.T_GON)<Angle(250,Angle.T_GON),' ... undefined!')
print('20>19   =',Angle(20,Angle.T_GON)>Angle(19,Angle.T_GON))
print('19>20   =',Angle(19,Angle.T_GON)>Angle(20,Angle.T_GON))
print('19>19   =',Angle(19,Angle.T_GON)>Angle(19,Angle.T_GON))
print('19>=19  =',Angle(19,Angle.T_GON)>=Angle(19,Angle.T_GON))
print('50>251  =',Angle(50,Angle.T_GON)>Angle(251,Angle.T_GON))
print('50>250  =',Angle(50,Angle.T_GON)>Angle(250,Angle.T_GON),' ... undefined!')
print('50==450 =',Angle(50,Angle.T_GON)==Angle(450,Angle.T_GON))
print('50!=450 =',Angle(50,Angle.T_GON)!=Angle(450,Angle.T_GON))
print('50!=451 =',Angle(50,Angle.T_GON)!=Angle(451,Angle.T_GON))
print('w1!=w2  =',w1!=w2)

# new tests 
print('w1 + 30:', w1 + 30)           # Valid addition with integer
print('w1 + "30":', w1 + "30")       # Valid addition with string numeric
print('w1 + 30.0:', w1 + 30.0)       # Valid addition with float
print('30 + w1:', 30 + w1)           # Valid addition with reverse operand
print('w1 - "30":', w1 - "30")       # Valid subtraction with string numeric
print('w1 * w2 =', w1 * w2)          # Multiplies the normalized values of w1 and w2
print('w1 * 3  =', w1 * 3)           # Multiplies w1 by 3
print('3 * w1  =', 3 * w1)           # Reverse multiplication
print('w1 / w2 =', w1 / w2)          # Returns the ratio of w1 to w2
print('w1 / 2  =', w1 / 2)           # Divides w1 by 2
print('3 / w1:', 3 / w1)            # Reverse division with non-zero angle
print('3.0 / w1:', 3.0 / w1)        # Reverse division with float



# Old tests using different angle definitions
w3=Angle(50,Angle.T_GON)
print('w2==4*w3=',w2==Angle(w3*4,Angle.T_GON))
print('0.001 is_similar -0.001 by 0.1',Angle.is_similar(-0.001,+0.001,0.1))
print('w1 is_similar w2 by 0.1',Angle.is_similar(w1,w2,0.1))
w1=Angle(150,Angle.T_GON)
w2=Angle(135,Angle.T_DEG)
print(w1)
print(w2)
print('w1 is_similar w2 by 0.1',Angle.is_similar(w1,w2,0.1))

#new tests with redefined angles:
print('atan2(-3, 2) =', w3.atan2(-3, 2, Angle.T_GON))

