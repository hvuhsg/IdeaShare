from uvicorn import run


def main():
    run("server:app", host="0.0.0.0", port=80)

if __name__ == "__main__":
    main()
