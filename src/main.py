from uvicorn import run


def main():
    run("server:app", host="127.0.0.1", port=80)

if __name__ == "__main__":
    main()
