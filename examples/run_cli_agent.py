from my_hello_agents.builder import build_full_react_agent


def main():
    agent = build_full_react_agent(verbose=True)

    print("HelloAgents CLI 已启动。")
    print("你可以输入问题，输入 exit / quit 退出。")
    print("-" * 50)

    while True:
        user_input = input("\n用户：").strip()

        if user_input.lower() in ["exit", "quit", "q"]:
            print("已退出。")
            break

        if not user_input:
            continue

        answer = agent.run(user_input)

        print("\n助手：")
        print(answer)

        print("\n本轮执行轨迹：")
        for step in agent.get_trace():
            print(step)


if __name__ == "__main__":
    main()