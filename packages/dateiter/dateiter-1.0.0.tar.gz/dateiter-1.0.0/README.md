# dateiter

<p align="center">
    <a href="https://github.com/yassun7010/dateiter/actions">
        <img src="https://github.com/yassun7010/dateiter/actions/workflows/test-suite.yml/badge.svg" alt="Test Suite">
    </a>
    <a href="https://pypi.org/project/dateiter">
        <img src="https://badge.fury.io/py/dateiter.svg" alt="PIP Version">
    </a>
</p>

Simple date iterator tool.

## Usage
```sh
for date in $(dateiter 2020-01-01 2020-01-05); do
    echo $date
done

# 2020-01-01
# 2020-01-02
# 2020-01-03
# 2020-01-04
```
