from random import randint

from application_context import ApplicationContext


def create_users(context: ApplicationContext):
    for i in range(1, 10):
        context.register(username=f'user{i}', password=f'pass{i}')


def create_messages(context: ApplicationContext):
    for i in range(1, 10):
        context.login(username=f'user{i}', password=f'pass{i}')
        for j in range(1, randint(2, 10)):
            message = f'Message {i} to {j}'
            context.send_message(to_user=f'user{j}', file=message.encode("utf-8"), file_type='text')


if __name__ == "__main__":
    context = ApplicationContext()
    # create_users(context)
    # create_messages(context)
