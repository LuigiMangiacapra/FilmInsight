import random

class EpsilonGreedyMAB:
    def __init__(self, epsilon=0.1, decay="none", min_epsilon=0.01, seed=None):
        """
        Inizializza l'algoritmo Epsilon-Greedy.

        Args:
            epsilon (float): Probabilità di esplorazione (valore iniziale).
            decay (str): Tipo di decadimento per epsilon ("none", "linear", "exponential").
            min_epsilon (float): Il valore minimo che epsilon può raggiungere durante la decadenza.
            seed (int): Seed opzionale per rendere il comportamento riproducibile.
        """
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay
        self.action_counts = {}  # Conta il numero di volte che un'azione è stata scelta
        self.action_values = {}  # Valori medi stimati per ogni azione

        if seed is not None:
            random.seed(seed)  # Imposta il seed per numeri casuali

    def select_action(self, actions):
        """
        Seleziona un'azione utilizzando l'algoritmo Epsilon-Greedy.

        Args:
            actions (list): Lista delle azioni disponibili.

        Returns:
            L'azione scelta.

        Raises:
            ValueError: Se la lista delle azioni è vuota.
        """
        if not actions:  # Controlla se la lista delle azioni è vuota
            raise ValueError("La lista delle azioni non può essere vuota.")

        # Esplorazione o sfruttamento
        if random.random() < self.epsilon:
            return random.choice(actions)  # Esplorazione (scelta casuale)
        else:
            # Sfruttamento: seleziona l'azione con il valore medio più alto
            return max(actions, key=lambda action: self.action_values.get(action, 0))

    def update(self, action, reward):
        """
        Aggiorna i valori stimati per un'azione in base alla ricompensa ricevuta.

        Args:
            action: L'azione eseguita.
            reward (float): La ricompensa ricevuta per l'azione.
        """
        if action not in self.action_counts:
            self.action_counts[action] = 0
            self.action_values[action] = 0

        # Aggiorna il conteggio delle volte che l'azione è stata scelta
        self.action_counts[action] += 1

        # Aggiorna il valore medio stimato dell'azione
        n = self.action_counts[action]
        self.action_values[action] += (reward - self.action_values[action]) / n

        # Aggiorna epsilon in base al tipo di decadimento scelto
        if self.decay == "exponential" and self.epsilon > self.min_epsilon:
            self.epsilon *= 0.99  # Decadimento esponenziale
        elif self.decay == "linear" and self.epsilon > self.min_epsilon:
            self.epsilon -= 0.001  # Decadimento lineare
            self.epsilon = max(self.epsilon, self.min_epsilon)

    def get_epsilon(self):
        """
        Restituisce il valore attuale di epsilon.

        Returns:
            float: Valore attuale di epsilon.
        """
        return self.epsilon

    def get_action_values(self):
        """
        Restituisce i valori stimati delle azioni.

        Returns:
            dict: Un dizionario con le azioni come chiavi e i valori stimati come valori.
        """
        return self.action_values

    def display_state(self):
        """
        Mostra lo stato corrente delle azioni, i loro valori stimati e i conteggi.
        """
        print("\nStato corrente:")
        print(f"Epsilon: {self.epsilon:.4f}")
        print("Azioni e valori stimati:")
        for action, value in self.action_values.items():
            count = self.action_counts.get(action, 0)
            print(f"  Azione: {action}, Valore stimato: {value:.4f}, Conteggio: {count}")
