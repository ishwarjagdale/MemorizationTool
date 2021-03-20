from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class FlashCard(Base):
    __tablename__ = "flashcard"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    box_number = Column(Integer, default=0, nullable=False)


class MemTool:

    def __init__(self):
        self.menu = {
            1: "Add flashcards",
            2: "Practice flashcards",
            3: "Exit"
        }
        funcs = {
            1: self.add,
            2: self.practice,
            3: self.exit

        }

        engine = create_engine("sqlite:///flashcard.db", connect_args={"check_same_thread": False})
        FlashCard.__table__.create(bind=engine, checkfirst=True)
        session = sessionmaker(bind=engine)
        self.db = session()

        while True:
            menu_opt = input("\n".join([f"{x}. {self.menu[x]}" for x in self.menu]) + "\n")
            try:
                menu_opt = int(menu_opt)
                if menu_opt not in self.menu:
                    raise ValueError
            except ValueError:
                print(f"\n{menu_opt} is not an option")
            else:
                while True:
                    if funcs[menu_opt]() is False:
                        break

    def add(self):
        menu = {1: "Add a new flashcard", 2: "Exit"}
        menu_opt = input("\n" + "\n".join([f"{x}. {menu[x]}" for x in menu]) + "\n")
        try:
            menu_opt = int(menu_opt)
            if menu_opt not in menu:
                raise ValueError
        except ValueError:
            print(f"\n{menu_opt} is not an option")
        else:
            if menu_opt == 2:
                return False
            print("")
            while True:
                question = input("Question:\n").strip()
                if len(question.strip()) != 0:
                    break
            while True:
                answer = input("Answer:\n").strip()
                if len(answer.strip()) != 0:
                    break
            try:
                self.db.add(FlashCard(question=question, answer=answer))
                self.db.commit()
            except SQLAlchemyError as e:
                print(e)
            print("")

    def practice(self):
        cards = self.db.query(FlashCard).all()
        if len(cards) == 0:
            print("\nThere is no flashcard to practice!\n")
            return False
        for i in cards:
            answer = input(f"\nQuestion: {i.question}\n"
                           f"press \"y\" to see the answer:\npress \"n\" to skip:\npress \"u\" to update:\n").strip().lower()
            if answer == 'y':
                print(f"\nAnswer: {i.answer}")
                check = input("press \"y\" if your answer is correct:\npress \"n\" if your answer is wrong:\n")
                if check == 'y':
                    i.box_number += 1
                    if i.box_number >= 2:
                        self.db.delete(i)
                    self.db.commit()
                elif check == 'n':
                    i.box_number = 0
                    self.db.commit()
            elif answer == 'n':
                print("")
                check = input("press \"y\" if your answer is correct:\npress \"n\" if your answer is wrong:\n")
                if check == 'y':
                    i.box_number += 1
                    if i.box_number >= 2:
                        self.db.delete(i)
                    self.db.commit()
                elif check == 'n':
                    i.box_number = 0
                    self.db.commit()
                continue
            elif answer == 'u':
                up_menu = input("press \"d\" to delete the flashcard:\n"
                                "press \"e\" to edit the flashcard:\n").lower()
                if up_menu == "d":
                    self.db.delete(i)
                    self.db.commit()
                elif up_menu == "e":
                    n_que = input(f"\ncurrent question: {i.question}\nplease write a new question:\n").strip()
                    n_ans = input(f"\ncurrent answer: {i.answer}\nplease write a new answer:\n").strip()
                    if len(n_que) != 0:
                        i.question = n_que
                        self.db.commit()
                    if len(n_ans) != 0:
                        i.answer = n_ans
                        self.db.commit()
            else:
                print(f"\n{answer} is not an option")
        print("")
        return False

    @staticmethod
    def exit():
        print("\nBye!")
        exit()


if __name__ == "__main__":
    MemTool()
