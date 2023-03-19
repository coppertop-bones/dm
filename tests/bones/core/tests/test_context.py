# **********************************************************************************************************************
#
#                             Copyright (c) 2011-2018 David Briant. All rights reserved.
#
# **********************************************************************************************************************


from bones.core.sentinels import Missing
from bones.core.context import context


def test_context():
    with context(debug=True):
        with context(fred=5):
            assert context.debug == True
            assert context.fred == 5
            with context(fred=6):
                assert context.fred == 6
            assert context.fred == 5
    assert context.debug == Missing
    assert context.fred == Missing



def main():
    test_context()


if __name__ == '__main__':
    main()
    print('pass')

