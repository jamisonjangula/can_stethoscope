import argparse


def main():
    parser = argparse.ArgumentParser('can_stetho', description="Runs insights on CAN data")
    parser.add_argument("import_data")

    args = parser.parse_args()
    print(f"{args} Hello!")
