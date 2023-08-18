# **CheeseType**

一个仅是为了方便调用，而自定义了许多常用类型的库。

## **介绍**

该库的类型分为2类：

1. 你可以使用`type()`或`isinstance(value, type)`获取它们确切的类，而不会获取到类似于`int`、`float`这样的基类。它们和`int(value)`、`float(value)`，无法转换时会抛出`ValueError`。

2. 继承于`Enum`的类型。

## **安装**

```bash
pip install CheeseType
```

## **使用**

```python
from CheeseType import Bool, PositiveInt, System

Bool('False') # False
PositiveInt('123') # 123
System('WINDOWS') # System.WINDOWS
```

## **函数**

由于目前内容较少，暂时先存放在本处。

### **`from CheeseType import *`**

- **`class Bool`**

    该方法返回的类型永远是`bool`而不是`Bool`。

    该方法会将`True`、`'True'`、`'TRUE'`和`'true'`视作`True`，将`False`、`'False'`、`'FALSE'`和`'false'`视作`False`。

- **`class PositiveInt(int)`**

    大于0的整数。

- **`class NonNegativeInt(int)`**

    大于等于0的整数。

- **`class NegativeInt(int)`**

    小于0的整数。

- **`class NonPositiveInt(int)`**

    小于等于0的整数。

- **`class PositiveFloat(float)`**

    大于0的浮点数。

- **`class NonNegativeFloat(float)`**

    大于等于0的浮点数。

- **`class NegativeFloat(float)`**

    小于0的浮点数。

- **`class NonPositiveFloat(float)`**

    小于等于0的浮点数。

- **`class System(Enum)`**

    - **`WINDOWS = 'WINDOWS'`**

    - **`MACOS = 'MACOS'`**

    - **`LINUX = 'LINUX`**

    - **`OTHER = 'OTHER'`**

### **`from CheeseType.network import *`**

- **`class Port(NonNegativeInt)`**

    端口号。

- **`class IPv4(str)`**

- **`class IPv6(str)`**

- **`class IP(str)`**
